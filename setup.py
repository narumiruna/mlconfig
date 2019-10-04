import os

from setuptools import find_packages, setup


def get_committed_date(tag):
    return tag.commit.committed_date


def get_version():
    return os.system('git describe --tags')


def main():
    setup(
        name='mlconfig',
        version=get_version(),
        author='Narumi',
        author_email='weaper@gamil.com',
        packages=find_packages(),
        install_requires=['pyyaml', 'git'],
    )


if __name__ == "__main__":
    main()
