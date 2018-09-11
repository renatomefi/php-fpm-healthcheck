import pytest

def test_invalid_option_exits_properly(host):
    cmd = host.run("php-fpm-healthcheck --invalid-option")
    assert cmd.rc == 3

    cmd = host.run("php-fpm-healthcheck --invalid-option=")
    assert cmd.rc == 3

def test_valid_with_empty_value_exits_properly(host):
    cmd = host.run("php-fpm-healthcheck --listen-queue-len=")
    assert cmd.rc == 3
    assert "option value must be an integer" in cmd.stderr

def test_valid_with_non_integer_value_exits_properly(host):
    cmd = host.run("php-fpm-healthcheck --listen-queue-len=abc")
    assert cmd.rc == 3
    assert "option value must be an integer" in cmd.stderr

def test_missing_fcgi(host):
    host.run("apk del fcgi")
    cmd = host.run("php-fpm-healthcheck")
    assert cmd.rc == 4
    assert "Make sure fcgi is installed" in cmd.stderr
    
    # Fail safe for other tests, maybe we could use a docker fixture
    # to start a new container everytime
    host.run("apk add --no-cache fcgi")
