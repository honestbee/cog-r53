FROM python:3.6-alpine

RUN adduser -h /home/bundle -D bundle
ENV BUNDLE_NAME=r53
ENV BUNDLE_DIR=/home/bundle/$BUNDLE_NAME/

COPY setup.py requirements.txt $BUNDLE_DIR
WORKDIR $BUNDLE_DIR

# install bundle dependencies
# (provides a chaching layer with dependencies)
RUN pip install -r requirements.txt

# Copy and install bundle code
COPY $BUNDLE_NAME/ $BUNDLE_DIR/$BUNDLE_NAME/
RUN pip install .
