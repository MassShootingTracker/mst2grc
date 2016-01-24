from setuptools import setup

exec(open("./package.py").read())

setup(name=APPNAME,
      version=__version__,
      description=DESCRIPTION,
      author=__author__,
      url=URL,
      requires=['Flask>=0.10.1', 'praw>=3.3.0', 'requests>=2.9.1'])