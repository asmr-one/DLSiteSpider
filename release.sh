rm -rf dist/ DLSiteSpider.egg-info/
python3 -m build
python3 -m twine upload --repository pypi dist/*
rm -rf dist/ DLSiteSpider.egg-info/