from setuptools import setup, find_packages

VERSION = 0.3

setup(
    name="common_helper_process",
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        'pexpect',
        'common_helper_files'
    ],
    dependency_links=[
        'git+https://github.com/fkie-cad/common_helper_files.git#common_helper_files'
    ],
    description="Helper functions for handling processes.",
    author="Fraunhofer FKIE",
    author_email="peter.weidenbach@fkie.fraunhofer.de",
    url="http://www.fkie.fraunhofer.de",
    license="GPL-3.0"
)
