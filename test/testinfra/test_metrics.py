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
    assert "Trying to connect to php-fpm via:" in cmd.stdout
    assert "status output:" in cmd.stdout
    assert "pool:" in cmd.stdout

@pytest.mark.php_fpm
def test_listen_queue_len_and_listen_queue_vars_are_parsed_correctly(host):
    cmd = host.run("php-fpm-healthcheck --verbose --listen-queue=5 --max-listen-queue=1024")
    assert cmd.rc == 0
    assert "Trying to connect to php-fpm via:" in cmd.stdout
    assert "'listen queue' value '0' and expected is less than '5" in cmd.stdout
    assert "'max listen queue' value '0' and expected is less than '1024'" in cmd.stdout

# @pytest.mark.php_fpm
# def test_multiple_custom_option_are_parsed_correctly(host):
#     This test should be only included when possible to use custom status page
#     cmd = host.run("FCGI_HEALTH_PARAMS=custom-param-one,custom-param-two php-fpm-healthcheck "
#                    "--verbose --custom-param-one=5 --custom-param-two=1024")
#     assert "Trying to connect to php-fpm via:" in cmd.stdout
#     assert "'custom param one' value '0' and expected is less than '5" in cmd.stdout
#     assert "'custom param two' value '0' and expected is less than '1024'" in cmd.stdout
