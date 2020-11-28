import pytest

@pytest.mark.php_fpm
def test_ping(host):
    cmd = host.run("php-fpm-healthcheck")
    assert cmd.rc == 0

@pytest.mark.php_fpm
def test_ping_verbose(host):
    cmd = host.run("php-fpm-healthcheck -v")
    assert cmd.rc == 0
    assert "Trying to connect to PHP-FPM via:" in cmd.stdout
    assert "PHP-FPM status output:" in cmd.stdout
    assert "pool:" in cmd.stdout
