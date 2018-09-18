FROM php:7.2-fpm-alpine3.8

# Required software
RUN apk add --no-cache fcgi

# Enable php fpm status page
RUN set -xe && echo "pm.status_path = /status" >> /usr/local/etc/php-fpm.d/zz-docker.conf

COPY ./php-fpm-healthcheck /usr/local/bin/
