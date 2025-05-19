from setuptools import setup, find_packages

setup(
    name='discord-bot',
    version='0.2',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
)