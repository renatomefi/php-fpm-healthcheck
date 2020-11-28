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
def test_valid_custom_option_with_empty_value_exits_properly(host):
    cmd = host.run("FCGI_HEALTH_PARAMS=custom-param php-fpm-healthcheck --verbose --custom-param=")
    assert cmd.rc == 3
    assert "option value must be an integer" in cmd.stderr

@pytest.mark.php_fpm
def test_valid_with_non_integer_value_exits_properly(host):
    cmd = host.run("php-fpm-healthcheck --listen-queue-len=abc")
    assert cmd.rc == 3
    assert "option value must be an integer" in cmd.stderr

@pytest.mark.php_fpm
def test_valid_custom_option_non_integer_value_exits_properly(host):
    cmd = host.run("FCGI_HEALTH_PARAMS=custom-param php-fpm-healthcheck --verbose --custom-param=abc")
    assert cmd.rc == 3
    assert "option value must be an integer" in cmd.stderr

@pytest.mark.php_fpm
def test_all_default_options_at_once(host):
    cmd = host.run("php-fpm-healthcheck --accepted-conn=1000 --listen-queue=1000 --max-listen-queue=1000 "
                   "--listen-queue-len=1000 --idle-processes=1000 --active-processes=1000 --total-processes=1000 "
                   "--max-active-processes=1000 --max-children-reached=1000 --slow-requests=1000")
    assert cmd.rc == 0

@pytest.mark.php_fpm
@pytest.mark.parametrize("option", [
    "accepted-conn",
    "listen-queue",
    "max-listen-queue",
    "idle-processes",
    "active-processes",
    "total-processes",
    "max-active-processes",
    "max-children-reached",
    "slow-requests",
])
def test_all_default_options(host, option):
    cmd = host.run("php-fpm-healthcheck --verbose --{0}=1000".format(option))
    assert cmd.rc == 0
    assert "value" in cmd.stdout
    assert "and expected is less than '1000'" in cmd.stdout

@pytest.mark.php_fpm
@pytest.mark.parametrize("option", [
    "accepted-conn",
    "listen-queue",
    "max-listen-queue",
    "idle-processes",
    "active-processes",
    "total-processes",
    "max-active-processes",
    "max-children-reached",
    "slow-requests",
])
def test_all_default_options_on_custom_list(host, option):
    cmd = host.run("FCGI_HEALTH_PARAMS={0} php-fpm-healthcheck --verbose --{0}=1000".format(option, option))
    assert cmd.rc == 0
    assert "value" in cmd.stdout
    assert "and expected is less than '1000'" in cmd.stdout

# @pytest.mark.php_fpm
# def test_custom_option(host):
#     This test should be only included when possible to use custom status page
#     cmd = host.run("FCGI_HEALTH_PARAMS=custom-param php-fpm-healthcheck --verbose --custom-param=1000")
#     assert cmd.rc == 0
#     assert "value" in cmd.stdout
#     assert "and expected is less than '1000'" in cmd.stdout

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
