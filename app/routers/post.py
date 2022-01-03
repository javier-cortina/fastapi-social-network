from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import oauth2
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    # In case we want to retrieve all posts (with filters and number of votes)
    posts = db.query(
            models.Post, func.count(models.Vote.post_id).label("votes")
        ).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True
        ).filter(
            models.Post.title.contains(search)
        ).group_by(
            models.Post.id
        ).limit(
            limit
        ).offset(
            skip
        ).all()
    
    # In case we want to retrieve only the logged-in user's posts
    # posts = db.query(models.Post).filter_by(owner_id=current_user.id).all()
    
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(
            models.Post, func.count(models.Vote.post_id).label("votes")
        ).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True
        ).filter(
            models.Post.id == id
        ).group_by(
            models.Post.id
        ).first()
    
    # post = db.query(models.Post).filter_by(id=str(id)).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter_by(id=str(id))
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    
    return {"message": "post was successfully deleted"}


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter_by(id=str(id))
    old_post = post_query.first()
    
    if old_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    if old_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()
