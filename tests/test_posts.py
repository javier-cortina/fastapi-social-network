import pytest
from app import schemas

## Get posts
def test_get_all_posts(authorized_client, test_posts):
    resp = authorized_client.get("/posts/")
    # posts = schemas.PostOut(resp.json())  # this doesn't work because it is a list of posts instead of 1 post (PostOut)
    # instead we can spread the list of posts to check the individual posts
    def validate(post):
        return schemas.PostOut(**post)
    
    posts_map = map(validate, resp.json())
    posts_list = list(posts_map)

    # we can verify the output simply by checking the lenght of the response
    assert len(resp.json()) == len(posts_list)
    assert resp.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):  # we pass client instead of authorized client, also we call test_posts just for the db to have some posts
    resp = client.get('/posts/')
    assert resp.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    resp = client.get(f'/posts/{test_posts[0].id}')
    assert resp.status_code == 401

def test_get_one_post_does_not_exist(authorized_client, test_posts):
    resp = authorized_client.get(f'/posts/88888')
    assert resp.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    resp = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = schemas.PostOut(**resp.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

## Create posts
@pytest.mark.parametrize("title, content, published",[
    ('awesome new title', 'awesome new content', True),
    ('favorite pizza', 'I love pepperoni', False),
    ('tallest skyscrapers', 'wahoo', True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    resp = authorized_client.post('/posts/', json={'title': title, 'content': content, 'published': published})
    created_post = schemas.Post(**resp.json())
    assert resp.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    resp = authorized_client.post('/posts/', json={'title': 'arbitrary title', 'content': 'arbitrary content'})
    created_post = schemas.Post(**resp.json())
    assert resp.status_code == 201
    assert created_post.title == 'arbitrary title'
    assert created_post.content == 'arbitrary content'
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client, test_user, test_posts):
    resp = client.post('/posts/', json={'title': 'arbitrary title', 'content': 'arbitrary content'})
    assert resp.status_code == 401

## Delete posts
def test_unauthorized_user_delete_post(client, test_user, test_posts):
    resp = client.delete(f'/posts/{test_posts[0].id}')
    assert resp.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    resp = authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert resp.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    resp = authorized_client.delete('/posts/88888')
    assert resp.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    resp = authorized_client.delete(f'/posts/{test_posts[3].id}')
    assert resp.status_code == 403

## Update posts
def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    resp = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**resp.json())
    assert resp.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    resp = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert resp.status_code == 403

def test_unauthorized_user_update_post(client, test_user, test_posts):
    resp = client.put(f'/posts/{test_posts[0].id}')
    assert resp.status_code == 401

def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    resp = authorized_client.put('/posts/88888', json=data)
    assert resp.status_code == 401  # changed this to cause error in CI/CD pipeline