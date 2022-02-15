FROM python:3

WORKDIR /usr/src/fastapi-app

COPY requirements_pro.txt ./

RUN pip install --no-cache-dir -r requirements_pro.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]