from setuptools import setup, find_packages

setup(
    name='page_query',
    version='0.1.2',
    py_modules=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'pq = page_query.main:main',
        ],
    },
)