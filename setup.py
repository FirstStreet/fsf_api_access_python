from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requirements = [x.strip() for x in f.readlines()]

with open('extra_test_requires.txt') as f:
    extra = {'testing': [x.strip() for x in f.readlines()]}

setup(
    name='firststreet-python',
    version='0.1',
    description='A Python API Client for the First Street Foundation API',
    url='https://github.com/FirstStreet/firststreet-python',
    project_urls={
        'First Street Foundation Website': 'https://firststreet.org/'
    },
    long_description=readme,

    # Package info
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    py_modules=[],
    install_requires=requirements,
    python_requires='>=3.6',
    extras_require=extra,
)
