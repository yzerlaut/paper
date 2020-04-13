import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

     name='finalyz',  

     version='0.1',

     scripts=['finalyz'] ,

     author="Zerlaut Yann",

     author_email="yann.zerlaut@gmail.com",

     description="A program to compile scientific documents",

     long_description=long_description,

   long_description_content_type="text/markdown",

     url="https://github.com/yzerlaut/finalyz",

     packages=setuptools.find_packages(),

     classifiers=[

         "Programming Language :: Python :: 3",

         "License :: OSI Approved :: MIT License",

         "Operating System :: OS Independent",

     ],

    install_requires=[
        "numpy",
        "bibtexparser",
        "argparse"
    ]
 )
