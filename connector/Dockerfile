FROM python:3.7

ARG VERSION="unknown"
ARG BUILDNUMBER="unknown"
ARG GITSHA1="unknown"

# environemnt variables
ENV VERSION=${VERSION} \
    BUILDNUMBER=${BUILDNUMBER} \
    GITSHA1=${GITSHA1} \
    STREAM=requests \
    RABBITMQ_QUEUE="ncsa.workbench.connector"

WORKDIR /extractor
#COPY requirements.txt ./
#RUN pip install -r requirements.txt

COPY pyclowder ./pyclowder
RUN pip install ./pyclowder && cd ..

RUN mkdir /home/worksman

COPY sidecar_extractor.py extractor_info.json ./
CMD python sidecar_extractor.py

