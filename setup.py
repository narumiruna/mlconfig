from setuptools import find_packages, setup


def main():
    setup(
        name='mlconfig',
        use_scm_version=True,
        setup_requires=['setuptools_scm'],
        author='Narumi',
        author_email='weaper@gamil.com',
        packages=find_packages(),
        install_requires=['pyyaml'],
    )


if __name__ == "__main__":
    main()
