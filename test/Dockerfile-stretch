FROM php:7.2-fpm-stretch

# Required software
RUN set -x \
    && apt-get update \
    && apt-get install -y libfcgi-bin

# Enable php fpm status page
RUN set -xe && echo "pm.status_path = /status" >> /usr/local/etc/php-fpm.d/zz-docker.conf

COPY ./php-fpm-healthcheck /usr/local/bin/
