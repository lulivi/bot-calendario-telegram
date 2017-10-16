"""Setup file."""

# external imports
from setuptools import setup

# long description
with open("README.md", 'r') as f:
    long_description = f.read()

# requirements
requirements = []

setup(
    name='bot-calendario-telegram',
    version='0.2',
    description='A telegram bot to keep every objective up to date.',
    long_description=long_description,
    license="GPLv3",
    author='Luis Liñán',
    author_email='luislivilla@gmail.com',
    url="https://github.com/lulivi/bot-calendario-telegram",
    install_requires=requirements, )
