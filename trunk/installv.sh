# install for current virtual environment.
pip uninstall pirs;

python setup.py clean
rm -rf dist/*

python setup.py sdist

# pip install -r requirements.txt dist/pirs*.tar.gz 
pip install dist/pirs*.tar.gz 

