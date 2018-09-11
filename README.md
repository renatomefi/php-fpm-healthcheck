# A PHP fpm Health Check script

With the ascension of containerized applications it becomes more and more useful to have a php-fpm `healthcheck`.

This POSIX compliant sh script gets php-fpm status page using `cgi-fcgi` tool, parses it's outcome and allows you to choose a metric which you want to check one, a ping mode is also available which only makes sure php-fpm is answering.

## Installation

### Download

```sh
curl -L -o /usr/local/bin/php-fpm-healthcheck \
https://raw.githubusercontent.com/renatomefi/php-fpm-healthcheck/master/php-fpm-healthcheck
```

### Update

```sh
curl -L -o $(which php-fpm-healthcheck) \
https://raw.githubusercontent.com/renatomefi/php-fpm-healthcheck/master/php-fpm-healthcheck
```

### Manually

You can always of course manually [download](https://raw.githubusercontent.com/renatomefi/php-fpm-healthcheck/master/php-fpm-healthcheck) and maintain the file, as long as you follow the [MIT License](./LICENSE)

## Why POSIX sh

Most of the containers contain limited software installed, using POSIX sh aims to be compatible with most of the OS images around.

## Author

Made with love by [Renato Mefi](https://github.com/renatomefi)
