FROM python:3.12-slim

WORKDIR /app

COPY load_data.py /app/

RUN pip install psycopg2-binary

CMD ["python", "load_data.py"]