import pytest

@pytest.mark.php_fpm
def test_metric_fail_accepted_conn(host):
    host.run("kill -USR2 1") # reset accepted conn value
    cmd = host.run("php-fpm-healthcheck --accepted-conn=0")
    assert cmd.rc == 1
    assert "'accepted conn' value '1' is greater than expected '0'" in cmd.stderr

@pytest.mark.php_fpm
def test_metric_fail_accepted_conn_with_other_metrics(host):
    cmd = host.run("php-fpm-healthcheck --verbose --listen-queue=10 --max-active-processes=10 --accepted-conn=0")
    assert cmd.rc == 1
    assert "'accepted conn' value '2' is greater than expected '0'" in cmd.stderr
    assert "'listen queue' value" in cmd.stdout
    assert "'max active processes' value" in cmd.stdout

@pytest.mark.php_fpm
def test_metric_accepted_conn(host):
    cmd = host.run("php-fpm-healthcheck -v")
    assert cmd.rc == 0
    assert "Trying to connect to PHP-FPM via:" in cmd.stdout
    assert "PHP-FPM status output:" in cmd.stdout
    assert "pool:" in cmd.stdout

@pytest.mark.php_fpm
def test_listen_queue_len_and_listen_queue_vars_are_parsed_correctly(host):
    cmd = host.run("php-fpm-healthcheck --verbose --listen-queue=5 --max-listen-queue=1024")
    assert cmd.rc == 0
    assert "Trying to connect to PHP-FPM via:" in cmd.stdout
    assert "'listen queue' value '0' and expected is less than '5" in cmd.stdout
    assert "'max listen queue' value '0' and expected is less than '1024'" in cmd.stdout
