import setuptools
from sqlalchemy_wrapper import get_version

VERSION = get_version()

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="sqlalchemy-wrapper",
    version=VERSION,
    license="BSL-1.1",
    author="coding kitties",
    description="A wrapper for sqlalchemy that helps in using sqlalchemy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coding-kitties/sqlalchemy-wrapper.git",
    download_url="https://github.com/coding-kitties/sqlalchemy-wrapper/archive/{}.tar.gz".format(get_version()),
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    keywords=['SQLALCHEMY', 'SQL', 'ORM', 'DATABASE'],
    classifiers=[
        "Intended Audience :: Developers",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=required,
    python_requires='>=3.6',
    include_package_data=True,
)
