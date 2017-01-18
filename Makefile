# gmake syntax
########################################################
# Makefile for Mongo Populator
#
# useful targets:
#   make deb-src -------------- produce a DEB source
#   make deb ------------------ produce a DEB
#   make docs ----------------- rebuild the manpages (results are checked in)
#   make tests ---------------- run the tests (see test/README.md for requirements)
#   make pyflakes, make pep8 -- source code checks

NAME = mongo-populator
OS = $(shell uname -s)

PYTHON=python

VERSION := $(shell cat VERSION | cut -f1 -d' ')

# Get the branch information from git
ifneq ($(shell which git),)
	GIT_DATE := $(shell git log -n 1 --format="%ai")
	GIT_HASH := $(shell git log -n 1 --format="%h")
	GIT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD | sed 's/[-_.\/]//g')
	GITINFO = .$(GIT_HASH).$(GIT_BRANCH)
else
	GITINFO = ""
endif

# DEB build parameters
DEBUILD_BIN ?= debuild
DEBUILD_OPTS = --source-option="-I"
DPUT_BIN ?= dput
DPUT_OPTS ?=
DEB_DATE := $(shell LC_TIME=C date +"%a, %d %b %Y %T %z")
ifeq ($(OFFICIAL),yes)
	DEB_RELEASE = $(RELEASE)ppa
	ifneq ($(DEBSIGN_KEYID),)
		DEBUILD_OPTS += -k$(DEBSIGN_KEYID)
	endif
else
	DEB_RELEASE = 100.git$(DATE)$(GITINFO)
	DEBUILD_OPTS += -uc -us
	DPUT_OPTS += -u
endif
DEBUILD = $(DEBUILD_BIN) $(DEBUILD_OPTS)
DEB_PPA ?= ppa
DEB_DIST ?= unstable

# Test parameters
MONGO_POPULATOR_TEST ?= test/runner/mongo-populator-test
PYTHON_VERSION ?= $(shell python3 -c 'import sys; print("%s.%s" % sys.version_info[:2])')

# Integration parameters (make integration)
IMAGE ?= centos7
TARGET ?=

########################################################

tests:
	$(MONGO_POPULATOR_TEST) units -v --python $(PYTHON_VERSION) $(TEST_FLAGS)

integration:
	$(MONGO_POPULATOR_TEST) integration -v --docker $(IMAGE) $(TARGET) $(TEST_FLAGS)

pep8:
	@echo "#############################################"
	@echo "# Running PEP8 Compliance Tests"
	@echo "#############################################"
	-pep8 -r --ignore=E501,E221,W291,W391,E302,E251,E203,W293,E231,E303,E201,E225,E261,E241 lib/populator/ bin/

pyflakes:
	pyflakes populator/*.py populator/*/*.py bin/*

clean:
	@echo "Cleaning up distutils stuff"
	rm -rf build
	rm -rf dist
	@echo "Cleaning up byte compiled python stuff"
	find . -type f -regex ".*\.py[co]$$" -delete
	@echo "Cleaning up editor backup files"
	find . -type f \( -name "*.swp" \) -delete
	@echo "Cleaning up output from test runs"
	rm -rf test/test_data
	@echo "Cleaning up Debian building stuff"
	rm -rf debian
	rm -rf deb-build
	rm -rf docs/json
	rm -rf docs/js

python:
	$(PYTHON) setup.py build

install:
	$(PYTHON) setup.py install

webdocs:
	(cd docs/docsite/; make docs)
