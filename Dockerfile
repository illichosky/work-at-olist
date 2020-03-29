FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /workatolist
WORKDIR /workatolist
COPY requirements.txt /workatolist/
RUN pip install -r requirements.txt
COPY . /workatolist/