FROM python:3.9-alpine

RUN apk add --no-cache socat
RUN pip3 install pycryptodome
RUN mkdir /app
COPY ./bigdata.py /
COPY ./flag.txt /

CMD socat -T 120 TCP-LISTEN:10000,reuseaddr,fork EXEC:"python3 /bigdata.py",stderr

EXPOSE 10000