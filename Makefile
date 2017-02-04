# gmake syntax
########################################################
# Makefile for Mongo Populator
#
# useful targets:
#   make tests ---------------- run the tests
#   make pyflakes, make pep8 -- source code checks
#   make install -------------- installs awesome mongo-populator

PYTHON=python3

########################################################

tests:
	$(PYTHON) setup.py test --verbose

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

install:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) setup.py install

