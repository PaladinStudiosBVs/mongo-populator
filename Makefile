PYTHON=python3

tests:
	$(PYTHON) setup.py test --verbose

pep8:
	@echo "#############################################"
	@echo "# Running PEP8 Compliance Tests"
	@echo "#############################################"
	-pep8 -r --ignore=E501,E221,W291,W391,E302,E251,E203,W293,E231,E303,E201,E225,E261,E241 lib/populator/ bin/

pyflakes:
	pyflakes populator/*.py populator/*/*.py bin/*

install:
	@mkdir -p /etc/mongo-populator
	@cp examples/mongo-populator.cfg /etc/mongo-populator/
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) setup.py install

clean:
	@rm -Rf lib/mongo_populator.egg-info
	@rm -Rf __pycache__
	@rm -Rf dist
	@rm -Rf build
	@rm -Rf .eggs

