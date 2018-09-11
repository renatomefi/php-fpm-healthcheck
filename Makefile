qa: lint test

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(abspath $(patsubst %/,%,$(dir $(mkfile_path))))

.PHONY: *

lint:
	docker run --rm -v ${current_dir}:/mnt:ro koalaman/shellcheck ./php-fpm-healthcheck

test:
	test -f php-fpm-healthcheck
