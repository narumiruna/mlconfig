import git
from setuptools import find_packages, setup


def get_committed_date(tag):
    return tag.commit.committed_date


def get_version():
    tags = git.Repo().tags
    tags = sorted(tags, key=get_committed_date, reverse=True)
    version = str(tags[0]).lstrip('v')
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
