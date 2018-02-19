pip uninstall pirs;

python setup.py clean
rm dist/*

python setup.py sdist

# if in virtualenv, do not use --user option:
if [ -z $VIRTUAL_ENV ]; then
    user="--user"
else
    user=""
fi;
pip install -e .
# pip install dist/pirs*.tar.gz $user

