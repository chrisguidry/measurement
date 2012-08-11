include virtualenvs.mk

all : python27 python32 pypy18
	$(PYTHON27)/bin/nosetests --with-doctest --with-coverage --cover-package=measurement --cover-inclusive --cover-erase

python27 :
	$(PYTHON27)/bin/nosetests --with-doctest

python32 :
	$(PYTHON32)/bin/nosetests --with-doctest

pypy18 :
	$(PYPY18)/bin/nosetests --with-doctest

bootstrap :
	$(PYTHON27)/bin/pip install -r requirements.txt
	$(PYTHON32)/bin/pip install -r requirements.txt
	$(PYPY18)/bin/pip install -r requirements.txt

clean :
	-find -name ".coverage" -exec rm '{}' ';'
	-find -name "*~" -exec rm '{}' ';'
	-find -name "*.*~" -exec rm '{}' ';'
	-find -name "*.pyc" -exec rm '{}' ';'
	-find -name "__pycache__" -exec rm -Rf '{}' ';'
