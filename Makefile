include virtualenvs.mk

all : python27 python32 pypy19 coverage

python27 :
	$(PYTHON27)/bin/nosetests --with-doctest

python32 :
	$(PYTHON32)/bin/nosetests --with-doctest

pypy19 :
	$(PYPY19)/bin/nosetests --with-doctest

coverage :
	$(PYTHON27)/bin/nosetests --with-doctest --with-coverage --cover-package=measurement --cover-inclusive --cover-erase

bootstrap :
	$(PYTHON27)/bin/pip install -r requirements.txt
	$(PYTHON32)/bin/pip install -r requirements.txt
	$(PYPY19)/bin/pip install -r requirements.txt

clean :
	-find -name ".coverage" -exec rm '{}' ';'
	-find -name "*~" -exec rm '{}' ';'
	-find -name "*.*~" -exec rm '{}' ';'
	-find -name "*.pyc" -exec rm '{}' ';'
	-find -name "__pycache__" -exec rm -Rf '{}' ';'
