import pytest

def test_ping(host):
    cmd = host.run("php-fpm-healthcheck")
    assert cmd.rc == 0

def test_ping_verbose(host):
    cmd = host.run("php-fpm-healthcheck -v")
    assert cmd.rc == 0
    assert "Trying to connect to php-fpm via:" in cmd.stdout
    assert "status output:" in cmd.stdout
    assert "pool:" in cmd.stdout
