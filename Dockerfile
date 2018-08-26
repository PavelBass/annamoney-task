FROM python:3
ENV PYTHONUNBUFFERED 1
ARG REQUIREMENTS_FILE=requirements.txt

RUN mkdir /annamoney_task
WORKDIR /annamoney_task

ADD ${REQUIREMENTS_SRC_PATH} /annamoney_task/
RUN pip install -e .
RUN pip install --no-cache-dir -r ${REQUIREMENTS_FILE}
ADD . /annamoney_task/

EXPOSE 8000
