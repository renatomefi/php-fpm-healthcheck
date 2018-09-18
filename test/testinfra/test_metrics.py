import pytest

@pytest.mark.php_fpm
def test_metric_accepted_conn(host):
    cmd = host.run("php-fpm-healthcheck -v")
    assert cmd.rc == 0
    assert "Trying to connect to php-fpm via:" in cmd.stdout
    assert "status output:" in cmd.stdout
    assert "pool:" in cmd.stdout
