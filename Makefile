# use system python to avoid pip interaction with virtualenv
PYTHON=/usr/bin/python

.PHONY: build
build: # build gh-access-token.pyz
build: *.py $(MAKEFILE_LIST)
	$(MAKE) clean
	mkdir -p build dist
	cp *.py build/
	$(PYTHON) -m pip --use-feature=2020-resolver install -r requirements.txt --target build
	find build -type d -name __pycache__ -exec rm -rf {} +
	# https://docs.python.org/3/library/zipapp.html
	$(PYTHON) -m zipapp --compress --output "dist/gh-access-token.pyz" build

.PHONY: clean
clean: # clean build output
	rm -rf build dist

.PHONY: help
help:  # Show help
	@grep -H -E '^[0-9A-Za-z_-]+:\s*#.*$$' $(MAKEFILE_LIST) | sort | \
		awk -F ':' '{ gsub(/\s*#/, "", $$3); printf "\033[37;1m%-20s\033[0m %s\n", $$2, $$3 }'
