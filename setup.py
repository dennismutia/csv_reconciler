from setuptools import setup, find_packages

setup(
    name="csv_reconciler",
    version="1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'csv_reconciler=csv_reconciler.cli:main'
        ]
    }
)