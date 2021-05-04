#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read()

setup(
    name='bch',
    version='@@VERSION@@',
    description='HARDWARIO Control Tool',
    author='HARDWARIO s.r.o.',
    author_email='karel.blavka@hardwario.com',
    url='https://github.com/hardwario/bch-control-tool',
    packages=['bch'],
    package_dir={'': '.'},
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    keywords=['HARDWARIO', 'TOWER', 'gateway', 'MQTT'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Communications',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Environment :: Console'
    ],
    entry_points='''
        [console_scripts]
        bch=bch.cli:main
    ''',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
