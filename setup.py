from setuptools import setup, find_packages

long_desc = """
Vodafone Scraper scrapes your current usage information from the My Vodafone
website.
"""
# See https://pypi.python.org/pypi?%3Aaction=list_classifiers for classifiers

setup(
    name='vodafone-scraper',
    version='1.0.0',
    description=("Scrapes your current usage information from the MyVodafone "
                 "website."),
    long_description=long_desc,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
    ],
    keywords='',
    author='Paul M Furley',
    author_email='paul@paulfurley.com',
    url='http://paulfurley.com',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'selenium>=2.32.0',
        'docopt>=0.6.1',
        'lxml>=3.2.0'
    ],
    tests_require=[],
    entry_points={
        'console_scripts': [
            'vodafone-scraper = vodafone_scraper.main:main',
        ]
    }
)
