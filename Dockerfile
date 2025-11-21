FROM python:3.11

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ .
EXPOSE 8000

CMD ["/bin/sh", "-c", "alembic -c /app/app/alembic.ini upgrade head && uvicorn main:main --host 0.0.0.0 --port 8000"]