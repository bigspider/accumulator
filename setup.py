from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='accumulator',
   version='1.0',
   description='A fast additive accumulator',
   license="MIT",
   long_description=long_description,
   author='Salvatore Ingala',
   author_email='salvatore.ingala@gmail.com',
   url="https://github.com/bigspider/accumulator",
   packages=['accumulator'],
   install_requires=[],
   scripts=[]
)
