#!/usr/bin/env python
import codecs
import os

from setuptools import find_packages, setup


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


setup(
    name='django-jellyglass',
    version='0.2.2',
    description='The ultimate Django admin honeypot.',
    long_description=read('README.rst'),
    author='Markus Holtermann',
    author_email='info@markusholtermann.eu',
    url='http://github.com/MarkusH/django-jellyglass',
    license='BSD',
    packages=find_packages(exclude=('tests.', 'tests', 'example')),
    include_package_data=True,
    install_requires=[
        'Django>=1.8',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
    ],
    zip_safe=False,
)
