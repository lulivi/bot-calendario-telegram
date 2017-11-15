"""Setup file."""

import os
from setuptools import setup, find_packages
from codecs import open

root_path = os.path.dirname(os.path.abspath(__file__))

# long description
with open(os.path.join(root_path, "README.md"), encoding='utf-8') as f:
    long_description = f.read()

# requirements
with open(os.path.join(root_path, 'requirements.txt'), encoding='utf-8') as f:
    requirements = list(filter(None, f.read().split('\n')))

setup(
    name='bot-calendario-telegram',
    version='0.4',
    description='A telegram bot to keep every objective up to date.',
    long_description=long_description,
    url="https://github.com/lulivi/bot-calendario-telegram",
    author='Luis Liñán',
    author_email='luislivilla@gmail.com',
    license="GPLv3",
    packages=find_packages(exclude=['docs', 'tests', 'data']),
    install_requires=requirements, )
