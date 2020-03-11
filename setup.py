import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

     name='paper',  

     version='0.1',

     scripts=['paper'] ,

     author="Zerlaut Yann",

     author_email="yann.zerlaut@gmail.com",

     description="A program to compile scientific documents",

     long_description=long_description,

   long_description_content_type="text/markdown",

     url="https://github.com/yzerlaut/paper",

     packages=setuptools.find_packages(),

     classifiers=[

         "Programming Language :: Python :: 3",

         "License :: OSI Approved :: MIT License",

         "Operating System :: OS Independent",

     ],

 )
