# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirments.txt requirments.txt

COPY .env .env

RUN pip3 install -r  requirments.txt

RUN pip3 install gunicorn

COPY . .




# Run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
