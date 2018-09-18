import pytest

@pytest.mark.php_fpm
def test_invalid_option_exits_properly(host):
    cmd = host.run("php-fpm-healthcheck --invalid-option")
    assert cmd.rc == 3

    cmd = host.run("php-fpm-healthcheck --invalid-option=")
    assert cmd.rc == 3

@pytest.mark.php_fpm
def test_valid_with_empty_value_exits_properly(host):
    cmd = host.run("php-fpm-healthcheck --listen-queue-len=")
    assert cmd.rc == 3
    assert "option value must be an integer" in cmd.stderr

@pytest.mark.php_fpm
def test_valid_with_non_integer_value_exits_properly(host):
    cmd = host.run("php-fpm-healthcheck --listen-queue-len=abc")
    assert cmd.rc == 3
    assert "option value must be an integer" in cmd.stderr

@pytest.mark.alpine
def test_missing_fcgi_apk(host):
    host.run("apk del fcgi")
    cmd = host.run("php-fpm-healthcheck")
    assert cmd.rc == 4
    assert "Make sure fcgi is installed" in cmd.stderr
    
    # Fail safe for other tests, maybe we could use a docker fixture
    # to start a new container everytime
    host.run("apk add --no-cache fcgi")

@pytest.mark.stretch
def test_missing_fcgi_apt(host):
    host.run("apt-get remove -y libfcgi-bin")
    cmd = host.run("php-fpm-healthcheck")
    assert cmd.rc == 4
    assert "Make sure fcgi is installed" in cmd.stderr
    
    # Fail safe for other tests, maybe we could use a docker fixture
    # to start a new container everytime
    host.run("apt-get install -y libfcgi-bin")
