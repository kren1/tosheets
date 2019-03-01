from setuptools import setup
from setuptools import find_packages

setup(
    name='tosheets',
    version='0.4.1',
    author='Timotej Kapus',
    author_email='kren1@users.noreply.github.com',
    description=('Cmd utility that send stdin to google sheets'),
    long_description=open('README.md').read(),
    license='MIT',
    keywords='utility sheets command line',
    url='https://github.com/kren1/tosheets',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ],
    install_requires=[
        'docopt',
        'oauth2client',
        'google-api-python-client'
    ],
    packages=find_packages(),
    package_data={'tosheets': ['client.json'] },
    entry_points={
        'console_scripts': [
            'tosheets = tosheets.tosheets:main'
        ],
    },

)
