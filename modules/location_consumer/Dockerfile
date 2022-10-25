FROM python:3.7-alpine

WORKDIR .

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev geos
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .
CMD ["python", "app/udaconnect/consumer.py"]