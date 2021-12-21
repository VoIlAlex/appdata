from setuptools import find_packages
from distutils.core import setup
import os

# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
	# Name of the package 
	name='appdata',
	# Packages to include into the distribution 
	packages=find_packages('.'),
	# Start with a small number and increase it with 
	# every change you make https://semver.org 
	version='2.1.1',
	# Chose a license from here: https: // 
	# help.github.com / articles / licensing - a - 
	# repository. For example: MIT 
	license='MIT',
	# Short description of your library 
	description='Utils to manage application data folder.',
	# Long description of your library 
	long_description=long_description,
	long_description_content_type='text/markdown',
	# Your name 
	author='voilalex',
	# Your email 
	author_email='ilya.vouk@gmail.com',
	# Either the link to your github or to your website 
	url='https://github.com/VoIlAlex/appdata',
	# Link from which the project can be downloaded 
	download_url='https://github.com/VoIlAlex/appdata/archive/v1.2.0.tar.gz',
	# List of keywords 
	keywords=[
		'utils', 'filesystem', 'paths', 'resources'
	],
	# List of packages to install with this one 
	install_requires=[
		'loguru==0.4.1',
		'pytest==6.2.5',
		'coveralls==3.3.1',
	],
	# https://pypi.org/classifiers/ 
	classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console :: Curses',
		'Topic :: Utilities',
		'Topic :: System :: Filesystems',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)
