.DEFAULT_GOAL := help
.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

ANSIBLE_PLATFORM ?= arm64
ANSIBLE_RELEASE ?= 10.0
PYTHON_RELEASE ?= 20240814
PYTHON_VERSION ?= 3.11.9

.PHONY: build
build: # Build binary using Docker
	docker buildx build \
		--platform linux/$(ANSIBLE_PLATFORM) \
		--build-arg ANSIBLE_RELEASE=$(ANSIBLE_RELEASE) \
		--build-arg PYTHON_RELEASE=$(PYTHON_RELEASE) \
		--build-arg PYTHON_VERSION=$(PYTHON_VERSION) \
		--progress=plain \
		--output dist src
