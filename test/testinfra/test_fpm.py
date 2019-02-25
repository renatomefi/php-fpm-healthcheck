import pytest

@pytest.fixture(scope="module")
def setup_fpm_fixture(host, request):
    print('Backing up current fpm configuration')
    host.run("cp /usr/local/etc/php-fpm.d/zz-docker.conf /tmp/zz-docker.conf")
    yield 1
    print('Recovering fpm configuration and reloading after module')
    host.run("cp /tmp/zz-docker.conf /usr/local/etc/php-fpm.d/zz-docker.conf")

@pytest.fixture
def setup_fpm_to_default_fixture(host, request, setup_fpm_fixture):
    print('Recovering fpm configuration and reloading')
    host.run("cp -f /tmp/zz-docker.conf /usr/local/etc/php-fpm.d/zz-docker.conf")
    host.run("kill -USR2 1")

@pytest.mark.php_fpm
def test_exit_when_no_status_page_is_configured(host, setup_fpm_to_default_fixture):
    # disable fpm status page
    host.run("sed -i /usr/local/etc/php-fpm.d/zz-docker.conf -e '/pm.status_path/ s/^;*/;/'")
    host.run("kill -USR2 1")
    
    cmd = host.run("php-fpm-healthcheck -v")
    assert cmd.rc == 8
    assert "Trying to connect to php-fpm via:" in cmd.stdout
    assert "status output:" in cmd.stdout
    assert "php-fpm status page non reachable" in cmd.stderr

@pytest.mark.php_fpm
def test_fpm_on_socket(host, setup_fpm_to_default_fixture):
    # change fpm to socket
    host.run("sed -i /usr/local/etc/php-fpm.d/zz-docker.conf -e '/^listen/ s/.*/listen = \\/var\\/run\\/php-fpm.sock/'")
    host.run("kill -USR2 1")
    
    cmd = host.run("FCGI_CONNECT=/var/run/php-fpm.sock php-fpm-healthcheck -v")
    assert cmd.rc == 0
    assert "Trying to connect to php-fpm via:" in cmd.stdout
    assert "status output:" in cmd.stdout
    assert "pool:" in cmd.stdout

# https://github.com/renatomefi/php-fpm-healthcheck/issues/18
@pytest.mark.php_fpm
def test_fpm_on_socket_with_huge_env(host, setup_fpm_to_default_fixture):
    cmd = host.run("HUGE_ENV=\"$(dd if=/dev/zero bs=8192 count=1 | tr '\\000' '\\040')\" php-fpm-healthcheck -v")
    assert cmd.rc == 0
    assert "Trying to connect to php-fpm via:" in cmd.stdout
    assert "status output:" in cmd.stdout
    assert "pool:" in cmd.stdout

@pytest.mark.alpine
def test_exit_when_fpm_is_not_reachable_apk(host, setup_fpm_to_default_fixture):
    cmd = host.run("FCGI_CONNECT=localhost:9001 php-fpm-healthcheck -v")
    assert cmd.rc == 9
    assert "Trying to connect to php-fpm via: localhost:9001" in cmd.stdout

@pytest.mark.alpine
def test_exit_when_fpm_is_invalid_host_apk(host, setup_fpm_to_default_fixture):
    cmd = host.run("FCGI_CONNECT=abc php-fpm-healthcheck -v")
    assert cmd.rc == 9
    assert "Trying to connect to php-fpm via: abc" in cmd.stdout

@pytest.mark.stretch
def test_exit_when_fpm_is_not_reachable_apt(host, setup_fpm_to_default_fixture):
    cmd = host.run("FCGI_CONNECT=localhost:9001 php-fpm-healthcheck -v")
    assert cmd.rc == 111
    assert "Trying to connect to php-fpm via: localhost:9001" in cmd.stdout

@pytest.mark.stretch
def test_exit_when_fpm_is_invalid_host_apt(host, setup_fpm_to_default_fixture):
    cmd = host.run("FCGI_CONNECT=abc php-fpm-healthcheck -v")
    assert cmd.rc == 2
    assert "Trying to connect to php-fpm via: abc" in cmd.stdout
