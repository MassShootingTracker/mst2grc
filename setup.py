from setuptools import setup
from pip.req import parse_requirements
import os

HERE = os.path.abspath(os.path.dirname(__file__))
exec(open(os.path.join(HERE, "package.py")).read())

install_reqs = parse_requirements(os.path.join(HERE, "requirements.txt"))
reqs = [str(ir.req) for ir in install_reqs]

setup(name=APPNAME,
      version=__version__,
      description=DESCRIPTION,
      author=__author__,
      url=URL,
      install_requires=reqs,
      requires=reqs)