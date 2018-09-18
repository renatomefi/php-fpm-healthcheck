import pytest

@pytest.mark.php_fpm
def test_exit_when_no_status_page_is_configured(host):
    # disable fpm status page
    host.run("sed -i /usr/local/etc/php-fpm.d/zz-docker.conf -e '/pm.status_path/ s/^;*/;/'")
    host.run("kill -USR2 1")
    
    cmd = host.run("php-fpm-healthcheck -v")
    assert cmd.rc == 8
    assert "Trying to connect to php-fpm via:" in cmd.stdout
    assert "status output:" in cmd.stdout
    assert "php-fpm status page non reachable" in cmd.stderr

    # enable fpm status page back
    host.run("sed -i /usr/local/etc/php-fpm.d/zz-docker.conf -e '/;pm.status_path/ s/^;*//'")
    host.run("kill -USR2 1")

@pytest.mark.php_fpm
def test_fpm_on_socket(host):
    # change fpm to socket
    host.run("sed -i /usr/local/etc/php-fpm.d/zz-docker.conf -e '/^listen/ s/.*/listen = \\/var\\/run\\/php-fpm.sock/'")
    host.run("kill -USR2 1")
    
    cmd = host.run("FCGI_CONNECT=/var/run/php-fpm.sock php-fpm-healthcheck -v")
    assert cmd.rc == 0
    assert "Trying to connect to php-fpm via:" in cmd.stdout
    assert "status output:" in cmd.stdout
    assert "pool:" in cmd.stdout

    # change fpm back to port 9000
    host.run("sed -i /usr/local/etc/php-fpm.d/zz-docker.conf -e '/^listen/ s/.*/listen = 9000/'")
    host.run("kill -USR2 1")

@pytest.mark.alpine
def test_exit_when_fpm_is_not_reachable_apk(host):
    cmd = host.run("FCGI_CONNECT=localhost:9001 php-fpm-healthcheck -v")
    assert cmd.rc == 9
    assert "Trying to connect to php-fpm via: localhost:9001" in cmd.stdout

@pytest.mark.alpine
def test_exit_when_fpm_is_invalid_host_apk(host):
    cmd = host.run("FCGI_CONNECT=abc php-fpm-healthcheck -v")
    assert cmd.rc == 9
    assert "Trying to connect to php-fpm via: abc" in cmd.stdout

@pytest.mark.stretch
def test_exit_when_fpm_is_not_reachable_apt(host):
    cmd = host.run("FCGI_CONNECT=localhost:9001 php-fpm-healthcheck -v")
    assert cmd.rc == 111
    assert "Trying to connect to php-fpm via: localhost:9001" in cmd.stdout

@pytest.mark.stretch
def test_exit_when_fpm_is_invalid_host_apt(host):
    cmd = host.run("FCGI_CONNECT=abc php-fpm-healthcheck -v")
    assert cmd.rc == 2
    assert "Trying to connect to php-fpm via: abc" in cmd.stdout
