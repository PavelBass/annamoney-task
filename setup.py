import os
from setuptools import setup, find_packages


setup(
    name='annamoney_task',
    version='0.0.1',
    author='Pavel Bass',
    author_email='statgg@gmail.com',
    description='anna.money job challenge',
    entry_points={
        'console_scripts': [
            'annamoney_task=annamoney_task.cli:cli',
        ],
    },
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    extras_require={
        'test': [
            'pycodestyle',
            'pylint',
            'pylint-quotes',
            'pytest',
            'pytest-cov',
            'pytest-mock',
            'pytest-asyncio',
            'diff-cover',
        ],
    },
)
