from setuptools import find_packages, setup


def parse_requirements(f):
    lines = []
    with open(f, 'r') as fp:
        for line in fp.readlines():
            lines.append(line.strip())
    return lines


def main():
    setup(
        name='mlconfig',
        version='0.1.1',
        author='Narumi',
        author_email='weaper@gamil.com',
        packages=find_packages(),
        install_requires=parse_requirements('requirements.txt'),
    )


if __name__ == "__main__":
    main()
