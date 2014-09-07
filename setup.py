from setuptools import setup, find_packages

__author__ = 'yluft'

setup(
    name='gamello',
    version='0.0.1.dev',
    description='Gamello is a gamefication engine for Trello boards',
    author='Roy Grossman, Daniel Jacobson, Yoav Luft',
    author_email='yoav.luft_at_gmail_dot_com',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    package_data={'resources': ['*']},
    install_requires=['requests']
)
