import pytest

@pytest.mark.php_fpm
def test_healthcheck_script_is_available(host):
    cmd = host.run("which php-fpm-healthcheck")
    assert cmd.rc == 0

@pytest.mark.php_fpm
def test_healthcheck_script_is_executable(host):
    scriptFile = host.check_output("which php-fpm-healthcheck")
      
    assert host.file(scriptFile).exists is True
    assert host.file(scriptFile).mode == 0o775
