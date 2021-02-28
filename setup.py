from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requirements = [x.strip() for x in f.readlines()]

with open('extra_test_requires.txt') as f:
    extra = {'testing': [x.strip() for x in f.readlines()]}

setup(
    name='fsf-api-access_python',
    version='2.3.1',
    description='A Python API Access Client for the First Street Foundation API',
    url='https://github.com/FirstStreet/fsf_api_access_python',
    project_urls={
        'First Street Foundation Website': 'https://firststreet.org/',
        'API Product Data Dictionary': 'https://docs.firststreet.dev/docs'
    },
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Kelvin",
    author_email="kelvin@firststreet.org",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Hydrology",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],

    # Package info
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    py_modules=[],
    install_requires=requirements,
    python_requires='>=3.7',
    extras_require=extra
)
