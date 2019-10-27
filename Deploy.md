
# For deploying to PyPI
```
# Make sure to install twine, setuptools and wheel
# Change the version-number in setup.py
python setup.py sdist bdist_wheel
python -m twine upload dist/*
```