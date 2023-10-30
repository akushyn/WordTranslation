FROM python:3.10-slim-buster

WORKDIR /app

RUN apt-get update \
  && apt-get install -y netcat gcc postgresql \
  && apt-get clean

RUN pip install --upgrade pip
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
