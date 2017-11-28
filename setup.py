"""Setup file."""

import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from codecs import open

root_path = os.path.dirname(os.path.abspath(__file__))


class PyTest(TestCommand):
    """Run test suite."""

    def initialize_options(self):
        """Initialize arguments to execute."""
        TestCommand.initialize_options(self)
        self.pytest_args = [
            '-v', '--pylama', '--cov-report=term-missing',
            '--cov=bot_calendario_telegram', 'tests/'
        ]

    def run_tests(self):
        """Run the suite."""
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


# long description
with open(os.path.join(root_path, "README.md"), encoding='utf-8') as f:
    long_description = f.read()

# requirements
with open(os.path.join(root_path, 'requirements.txt'), encoding='utf-8') as f:
    requirements = list(filter(None, f.read().split('\n')))

# test requirements
with open(
        os.path.join(root_path, 'test_requirements.txt'),
        encoding='utf-8') as f:
    test_requirements = list(filter(None, f.read().split('\n')))

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
    install_requires=requirements,
    tests_require=test_requirements,
    cmdclass={'test': PyTest},
)
