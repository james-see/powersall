from setuptools import setup, find_packages
import re

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('powersall/powersall.py').read(),
    re.M
).group(1)

setup(
    name='powersall',
    author='James Campbell',
    author_email='jc@normail.co',
    version=version,
    license='MIT',
    description='file extension info',
    packages=['powersall'],
    py_modules=['powersall'],
    keywords=['powerball', 'lottery',
              'random-numbers', 'lotto', 'megamillions'],
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    include_package_data=True,
    install_requires=[
        'beautifulsoup4',
        'requests',
        'lxml',
        'pandas',
        'argparse',
        'pathlib'
    ],
    entry_points={
        'console_scripts': [
            'powersall=powersall.powersall:main',
        ],
    },
    url='https://github.com/jamesacampbell/powersall',
    download_url='https://github.com/jamesacampbell/powersall/archive/{}.tar.gz'.format(
        version)
)
