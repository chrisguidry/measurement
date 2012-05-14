include virtualenvs.mk

.PHONY : tests
tests :
	$(PYTHON27)/bin/nosetests --with-doctest --with-coverage --cover-package=measurement --cover-inclusive --cover-erase
	$(PYTHON32)/bin/nosetests --with-doctest --with-coverage --cover-package=measurement --cover-inclusive --cover-erase

.PHONY : clean
clean :
	-find -name ".coverage" -exec rm '{}' ';'
	-find -name "*~" -exec rm '{}' ';'
	-find -name "*.*~" -exec rm '{}' ';'
	-find -name "*.pyc" -exec rm '{}' ';'

.PHONY : bootstrap
bootstrap :
	$(PYTHON27)/bin/pip install -r requirements.txt
	$(PYTHON32)/bin/pip install -r requirements.txt
