import subprocess

from setuptools import find_packages, setup


def get_version():
    tag = subprocess.check_output(['git', 'describe', '--tags']).decode('utf-8')
    version = tag.lstrip('v').split('-')[0]
    return version


def main():
    setup(
        name='mlconfig',
        version=get_version(),
        author='Narumi',
        author_email='weaper@gamil.com',
        packages=find_packages(),
        install_requires=['pyyaml'],
    )


if __name__ == "__main__":
    main()
