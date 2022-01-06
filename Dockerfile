FROM python:3.8.5-slim

RUN apt-get update && apt-get install libgomp1

COPY ["./deploy/requirements.txt", "/usr/src/webapp/"]

RUN /usr/local/bin/python -m pip install --upgrade pip

WORKDIR /usr/src/webapp

RUN pip install -r requirements.txt

COPY ["./deploy/", "/usr/src/webapp"]

EXPOSE 5000

CMD ["flask","run","--host=0.0.0.0"]


