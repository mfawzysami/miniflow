from setuptools import setup


def read(name):
    with open(name, 'r') as input:
        return input.read()


def requirements():
    with open('requirements.txt', 'r') as req:
        return req.readlines()


setup(
    name="Miniflow Python Package",
    version="0.0.9",
    author="Mohamed Fawzy",
    author_email="mfawzy.sami@gmail.com",
    description="Official Python Package for Mini Bioinformatics workflow wrapper (Miniflow)",
    license="BSD",
    keywords="miniflow",
    url="https://github.com/mfawzysami/miniflow",
    packages=["miniflow"],
    install_requires=requirements(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
