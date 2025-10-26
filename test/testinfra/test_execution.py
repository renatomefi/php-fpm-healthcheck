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

@pytest.mark.php_fpm
def test_all_available_options_at_once(host):
    cmd = host.run("php-fpm-healthcheck --accepted-conn=100000 --listen-queue=100000 --max-listen-queue=100000 "
                   "--listen-queue-len=100000 --idle-processes=100000 --active-processes=100000 --total-processes=100000 "
                   "--max-active-processes=100000 --max-children-reached=100000 --slow-requests=100000")
    assert cmd.rc == 0    

@pytest.mark.php_fpm
@pytest.mark.parametrize("option", [
    "--accepted-conn",
    "--listen-queue",
    "--max-listen-queue",
    "--idle-processes",
    "--active-processes",
    "--total-processes",
    "--max-active-processes",
    "--max-children-reached",
    "--slow-requests",
])
def test_all_available_options(host, option):
    cmd = host.run("php-fpm-healthcheck --verbose {0}=1000".format(option))
    assert cmd.rc == 0
    assert "value" in cmd.stdout
    assert "and expected is less than '1000'" in cmd.stdout

@pytest.mark.php_fpm
def test_fcgi_connect_option(host):
    cmd = host.run("php-fpm-healthcheck --fcgi-connect=127.0.0.1:9000")
    assert cmd.rc == 0

@pytest.mark.php_fpm
def test_fcgi_status_path_option(host):
    cmd = host.run("php-fpm-healthcheck --fcgi-status-path=/status")
    assert cmd.rc == 0

@pytest.mark.php_fpm
def test_fcgi_options_combined(host):
    cmd = host.run("php-fpm-healthcheck --fcgi-connect=localhost:9000 --fcgi-status-path=/status --accepted-conn=100000")
    assert cmd.rc == 0

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
