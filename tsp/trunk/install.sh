pip uninstall tsp;

python setup.py clean
rm dist/*

python setup.py sdist

pip install dist/tsp*.tar.gz --user

