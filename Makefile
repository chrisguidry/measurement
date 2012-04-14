.PHONY : tests
tests :
	nosetests --with-doctest --with-coverage --cover-package=measurement --cover-inclusive --cover-erase

.PHONY : clean
clean :
	-find -name ".coverage" -exec rm '{}' ';'
	-find -name "*~" -exec rm '{}' ';'
	-find -name "*.*~" -exec rm '{}' ';'
	-find -name "*.pyc" -exec rm '{}' ';'
