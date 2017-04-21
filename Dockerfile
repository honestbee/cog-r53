FROM python:3.6-alpine

RUN adduser -h /home/bundle -D bundle
ENV BUNDLE_NAME=r53
ENV BUNDLE_DIR=/home/bundle/$BUNDLE_NAME/

COPY setup.py requirements.txt $BUNDLE_DIR
WORKDIR $BUNDLE_DIR

RUN pip install -r requirements.txt
COPY $BUNDLE_NAME/ $BUNDLE_DIR/$BUNDLE_NAME/
