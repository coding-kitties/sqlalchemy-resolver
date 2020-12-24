import os
import shutil
from yolk.pypi import CheeseShop

PACKAGE_NAME = 'sqlalchemy_resolver'


def get_latest_version_number(package_name):
    pkg, all_versions = CheeseShop().query_versions_pypi(package_name)
    if len(all_versions):
        return all_versions[0]
    return None


if __name__ == "__main__":
    import sys

    sys.path.append('../')

    from sqlalchemy_resolver import get_version
    released_version = get_latest_version_number(PACKAGE_NAME)

    if released_version != get_version():
        os.chdir("../")

        # Remove distribution directory if exists
        if os.path.isdir('dist'):
            shutil.rmtree('dist')

        os.system("python setup.py sdist bdist_wheel")
        os.system("twine upload -r sqlalchemy-resolver dist/*")
        os.system("twine upload -p $pipy_password -u $pipy_username dist/*")