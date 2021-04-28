PYTHON ?= python3

SCRIPT = manetu-ql
SRCS = $(SCRIPT) $(shell find mql -name \*.py)

VERSION = $(shell cat mql/version.py | grep "version =" | cut -d " " -f3| tr -d "'")
BDISTWHEEL = dist/manetu-ql-$(VERSION)-py3-none-any.whl

.PHONY: all clean distclean dist sdist

all: bdist

clean:
	$(PYTHON) setup.py clean
	@rm -rf mql/__pycache__
	@rm -rf mql/commands/__pycache__
	@rm -rf mql/commands/graphql/__pycache__

distclean: clean
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info/

bdist: $(BDISTWHEEL)

$(BDISTWHEEL): setup.py $(SRCS)
	$(PYTHON) setup.py bdist_wheel

sdist: setup.py $(SRCS)
	$(PYTHON) setup.py sdist
