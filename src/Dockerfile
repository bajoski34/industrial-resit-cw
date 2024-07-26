FROM python:3.9

COPY . /code

WORKDIR /code

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN chmod +x /code/wait-for-it.sh

CMD ["./wait-for-it.sh", "bk_mysql:3306", "--timeout=30", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
