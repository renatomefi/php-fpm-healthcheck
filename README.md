# A PHP fpm Health Check script

With the ascension of containerized applications it becomes more and more useful to have a php-fpm `healthcheck`.

This POSIX compliant sh script gets php-fpm status page using `cgi-fcgi` tool, parses it's outcome and allows you to choose a metric which you want to check one, a ping mode is also available which only makes sure php-fpm is answering.

- [Installation](#installation)
- [Usage](#usage)
- [Kubernetes example](#kubernetes-example)
- [Why POSIX sh?](#why-posix-sh)
- [Author and License](#author)

## Installation

### Enable php-fpm status page

On you php-fpm pool configuration add: `pm.status_path = /status`

For instance on the official php image you can alter the file `/usr/local/etc/php-fpm.d/zz-docker.conf`

[See a simple example](https://github.com/renatomefi/php-fpm-healthcheck/blob/master/test/Dockerfile#L7)

[More about PHP fpm pool configuration](http://php.net/manual/en/install.fpm.configuration.php)

### Requirements

The script is POSIX sh but also uses some tools from your operating system, being:

- cgi-fcgi
- sed
- tail
- grep

In case you're using alpine you only need to make sure you have installed `busybox` and `fcgi` packages.

[See a simple Dockerfile based on the official PHP image](https://github.com/renatomefi/php-fpm-healthcheck/blob/master/test/Dockerfile)

### Download

```sh
wget -O /usr/local/bin/php-fpm-healthcheck \
https://raw.githubusercontent.com/renatomefi/php-fpm-healthcheck/master/php-fpm-healthcheck \
&& chmod +x /usr/local/bin/php-fpm-healthcheck
```

### Update

```sh
wget -O $(which php-fpm-healthcheck) \
https://raw.githubusercontent.com/renatomefi/php-fpm-healthcheck/master/php-fpm-healthcheck \
&& chmod +x $(which php-fpm-healthcheck)
```

### Manually

You can always of course manually [download](https://raw.githubusercontent.com/renatomefi/php-fpm-healthcheck/master/php-fpm-healthcheck) and maintain the file, as long as you follow the [MIT License](./LICENSE)

## Usage

### Ping mode

If you're aiming only to make sure php-fpm is alive and answering to requests you can:

```console
$ php-fpm-healthcheck
$ echo $?
0
```

Or with `verbose` to see php-fpm status output:

```console
$ php-fpm-healthcheck -v
Trying to connect to php-fpm via: localhost:9000
php-fpm status output:
pool:                 www
process manager:      dynamic
start time:           11/Sep/2018:10:47:06 +0000
start since:          436
accepted conn:        1
listen queue:         0
max listen queue:     0
listen queue len:     0
idle processes:       1
active processes:     1
total processes:      2
max active processes: 1
max children reached: 0
slow requests:        0
$ echo $?
0
```

### Metric mode

Let's say you want to fail our healthcheck after your fpm has handled more than `3000` requests:

```console
$ php-fpm-healthcheck --accepted-conn=3000
$ echo $?
0
```

And you can also check if you have more than `10` processes in the queue:

```console
$ php-fpm-healthcheck --accepted-conn=3000 --listen-queue-len=10
$ echo $?
0
```

#### How a failing metric looks like

```console
$ php-fpm-healthcheck --accepted-conn=1
'accepted conn' value '6' is greater than expected '1'
$ echo $?
1
```

### Connection via socket or another host

You can simply specify `FCGI_CONNECT` variable with your connection uri:

```console
$ FCGI_CONNECT=/var/run/php-fpm.sock php-fpm-healthcheck
$ echo $?
0
```

## Kubernetes example

More and more people are looking for health checks on kubernetes for php-fpm, here is an example of livenessProbe and readinessProbe:

### livenessProbe

```yaml
# PodSpec: https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.10/#podspec-v1-core
    spec:
        containers:
        - name: "php-fpm"
        livenessProbe:
            exec:
                command:
                    - php-fpm-healthcheck
                    - --listen-queue-len=10 # fails if there are more than 10 processes waiting in the fpm queue
                    - --accepted-conn=5000 # fails after fpm has served more than 5k requests, this will force the pod to reset, use with caution
            initialDelaySeconds: 0
            periodSeconds: 10
```

### readinessProbe

```yaml
# PodSpec: https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.10/#podspec-v1-core
    spec:
        containers:
        - name: "php-fpm"
        readinessProbe:
            exec:
                command:
                    - php-fpm-healthcheck # a simple ping since this means it's ready to handle traffic
            initialDelaySeconds: 1
            periodSeconds: 5
```

## Why POSIX sh

Most of the containers contain limited software installed, using POSIX sh aims to be compatible with most of the OS images around.

## Author

Made with love by [Renato Mefi](https://github.com/renatomefi)

Distributed under [MIT License](LICENSE)
