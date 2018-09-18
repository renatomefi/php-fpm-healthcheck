qa: lint test

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(abspath $(patsubst %/,%,$(dir $(mkfile_path))))

.PHONY: *

lint: php-fpm-healthcheck
	docker run --rm -v ${current_dir}:/mnt:ro koalaman/shellcheck \
	./php-fpm-healthcheck ./test/*.sh

test:
	$(MAKE) test-image IMAGE="php:fpm-alpine" DOCKERFILE="alpine"
	$(MAKE) test-image IMAGE="php:7.1-fpm-alpine3.7" DOCKERFILE="alpine"
	$(MAKE) test-image IMAGE="php:7.1-fpm-alpine3.8" DOCKERFILE="alpine"
	$(MAKE) test-image IMAGE="php:7.2-fpm-alpine3.7" DOCKERFILE="alpine"
	$(MAKE) test-image IMAGE="php:7.2-fpm-alpine3.8" DOCKERFILE="alpine"
	$(MAKE) test-image IMAGE="php:7.3-rc-fpm-alpine3.8" DOCKERFILE="alpine"
	$(MAKE) test-image IMAGE="php:7.1-fpm-stretch" DOCKERFILE="stretch"
	$(MAKE) test-image IMAGE="php:7.2-fpm-stretch" DOCKERFILE="stretch"
	$(MAKE) test-image IMAGE="php:7.3-rc-fpm-stretch" DOCKERFILE="stretch"

test-image:
	./test/docker.sh ${DOCKERFILE} ${IMAGE}
