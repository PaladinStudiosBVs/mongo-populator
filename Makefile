########################################################
# Makefile for Ansible
#
# useful targets:
#   make sdist ---------------- produce a tarball
#   make srpm ----------------- produce a SRPM
#   make rpm  ----------------- produce RPMs
#   make deb-src -------------- produce a DEB source
#   make deb ------------------ produce a DEB
#   make docs ----------------- rebuild the manpages (results are checked in)
#   make tests ---------------- run the tests (see test/README.md for requirements)
#   make pyflakes, make pep8 -- source code checks

NAME = mongo_populator
OS = $(shell uname -s)

MONGO_POPULATOR_TEST ?= test/runner/mongo_populator-test
PYTHON_VERSION ?= $(shell python3 -c 'import sys; print("%s.%s" % sys.version_info[:2])')

########################################################

tests:
        $(MONGO_POPULATOR_TEST) units -v --python $(PYTHON_VERSION) $(TEST_FLAGS)

integration:
        $(MONGO_POPULATOR_TEST) integration -v --docker $(IMAGE) $(TARGET) $(TEST_FLAGS)
