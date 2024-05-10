FROM python:3.7-alpine

ARG VERSION="unknown"
ARG BUILDNUMBER="unknown"
ARG GITSHA1="unknown"

# environment variables
ENV VERSION=${VERSION} \
    BUILDNUMBER=${BUILDNUMBER} \
    GITSHA1=${GITSHA1} \
    CLOWDER_VERSION=2 \
    RABBITMQ_QUEUE="ncsa.workbench.connector"

WORKDIR /extractor

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ncsa.workbench.connector.py extractor_info.json ./
CMD python ncsa.workbench.connector.py
