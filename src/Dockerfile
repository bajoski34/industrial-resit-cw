FROM python:3.9

COPY . /code

WORKDIR /code

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN chmod +x /code/wait-for-it.sh

CMD ["sh", "-c", "./wait-for-it.sh bk_mysql:3306 --timeout=30 --strict -- echo 'Running Migrations' && python infrastructure/migrate.py && uvicorn app.main:app --host 0.0.0.0 --port 80"]
