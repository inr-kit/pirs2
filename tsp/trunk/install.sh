pip uninstall tsp;

python setup.py clean
rm dist/*

python setup.py sdist

pip install -e .

