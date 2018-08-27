FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /annamoney_task
WORKDIR /annamoney_task

ADD ${REQUIREMENTS_SRC_PATH} /annamoney_task/
RUN pip install -e .
ADD . /annamoney_task/

EXPOSE 8000
