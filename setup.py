from importlib.machinery import SourceFileLoader

from setuptools import find_packages, setup

version = SourceFileLoader('version', 'mati/version.py').load_module()


with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='mati',
    version=version.__version__,
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='Client library for mati.io',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/mati-python',
    packages=find_packages(),
    include_package_data=True,
    package_data=dict(mati=['py.typed']),
    python_requires='>=3.6',
    install_requires=[
        'dataclasses>=0.6;python_version<"3.7"',
        'requests>=2.22.0,<3.0.0',
        'iso8601>=0.1.12,<0.2.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
