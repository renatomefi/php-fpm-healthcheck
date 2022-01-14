qa: lint test ## Lint and test the code in multiple images

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(abspath $(patsubst %/,%,$(dir $(mkfile_path))))

.PHONY: *

lint: php-fpm-healthcheck ## Lint code
	docker run --rm -v ${current_dir}:/mnt:ro koalaman/shellcheck \
	./php-fpm-healthcheck ./test/*.sh

test: ## Test code in multiple images
	$(MAKE) test-image IMAGE="php:7.1-fpm-alpine" DOCKERFILE="alpine"
	$(MAKE) test-image IMAGE="php:7.2-fpm-alpine" DOCKERFILE="alpine"
	$(MAKE) test-image IMAGE="php:7.3-fpm-alpine" DOCKERFILE="alpine"
	$(MAKE) test-image IMAGE="php:7.4-fpm-alpine" DOCKERFILE="alpine"
	$(MAKE) test-image IMAGE="php:8.0-fpm-alpine" DOCKERFILE="alpine"
	$(MAKE) test-image IMAGE="php:8.1-fpm-alpine" DOCKERFILE="alpine"
	$(MAKE) test-image IMAGE="php:7.1-fpm-stretch" DOCKERFILE="stretch"
	$(MAKE) test-image IMAGE="php:7.2-fpm-stretch" DOCKERFILE="stretch"
	$(MAKE) test-image IMAGE="php:7.3-fpm-stretch" DOCKERFILE="stretch"
	$(MAKE) test-image IMAGE="php:7.4-fpm-buster" DOCKERFILE="buster"
	$(MAKE) test-image IMAGE="php:8.0-fpm-buster" DOCKERFILE="buster"
	$(MAKE) test-image IMAGE="php:8.1-fpm-buster" DOCKERFILE="buster"

test-image:
	./test/docker.sh ${DOCKERFILE} ${IMAGE}

help:
	@echo "\033[33mUsage:\033[0m\n  make [target] [FLAGS=\"val\"...]\n\n\033[33mTargets:\033[0m"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[32m%-18s\033[0m %s\n", $$1, $$2}' #look at this magic
