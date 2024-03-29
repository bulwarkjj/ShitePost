# syntax=docker/dockerfile:1

FROM python:3.10-slim-bookworm
WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=app.py 
CMD ["flask", "run", "--host", "0.0.0.0"]