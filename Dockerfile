FROM python:3.11.9-alpine
LABEL authors="sakurademon"

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

CMD ["opentelemetry-instrument", "--logs_exporter", "otlp", "--service_name", "rolldice", "flask", "run", "--host=0.0.0.0"]