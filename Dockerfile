FROM python:3.8.2-buster

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt
COPY . /usr/src/app

RUN pip install -r requirements.txt

RUN \
    apt-get update && \
    apt-get install -y imagemagick && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# WARN: Following commands introduce vulnerability (DON'T DO THIS FOR PRODUCTION)
RUN sed -i -e 's/<policy domain="delegate" rights="none" pattern="HTTPS" \/>/<policy domain="delegate" rights="*" pattern="HTTPS" \/>/' /etc/ImageMagick-6/policy.xml
RUN sed -i -e 's/<policy domain="delegate" rights="none" pattern="HTTP" \/>/<policy domain="delegate" rights="*" pattern="HTTP" \/>/' /etc/ImageMagick-6/policy.xml