import pytest

@pytest.mark.php_fpm
def test_timeout_success(host):
    cmd = host.run("php-fpm-healthcheck --timeout=1")
    assert cmd.rc == 0

@pytest.mark.php_fpm
def test_timeout_without_value(host):
    cmd = host.run("php-fpm-healthcheck --timeout")
    assert cmd.rc == 3
    assert "timeout" in cmd.stderr
    assert "requires an argument" in cmd.stderr

@pytest.mark.php_fpm
def test_timeout_without_value(host):
    cmd = host.run("php-fpm-healthcheck --timeout=")
    assert cmd.rc == 3
    assert "--timeout" in cmd.stderr
    assert "option value must be an integer" in cmd.stderr

@pytest.mark.php_fpm
def test_timeout_invalid_value(host):
    cmd = host.run("php-fpm-healthcheck --timeout=abc")
    assert cmd.rc == 3
    assert "--timeout" in cmd.stderr
    assert "option value must be an integer" in cmd.stderr

# TODO test timeout command not found

@pytest.mark.php_fpm
def test_timeout_sleep(host):
    host.run("echo '<?php sleep(2);' > /var/www/html/sleep.php")
    cmd = host.run("FCGI_STATUS_PATH=/var/www/html/sleep.php php-fpm-healthcheck --timeout=1")
    # cmd.rc == 124 (coreutils)
    # cmd.rc == 129 (busybox)
    assert cmd.rc in [124, 129]
