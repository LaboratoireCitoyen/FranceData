import os
from setuptools import setup, find_packages, Command


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='francedata',
    version='0.0.1',
    description='Extracted data from French parliament',
    author='James Pic',
    author_email='jamespic@gmail.com',
    url='http://github.com/SocieteCitoyenne/FranceData',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    long_description=read('README.rst'),
    license='MIT',
    keywords='django france',
    install_requires=[
        'django-representatives-votes>=0.0.15',
        'django>=1.8,<1.9',
        'djangorestframework',
        'scrapy'
    ],
    extras_require={
    },
    classifiers=[
        'Development Status :: 1 - Alpha/Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
