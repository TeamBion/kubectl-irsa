import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='kubectl-irsa',  
     version='0.1',
     author="WoodProgrammer",
     description="IRSA control check via kubectl",
     long_description=long_description,
     long_description_content_type="text/markdown",
      install_requires=[
          "boto3",
          "pyyaml"
        ],
     url="https://github.com/WoodProgrammer/kubeirsa/",
     packages=setuptools.find_packages(),
     entry_points ={
            'console_scripts': [
                'kubectl-irsa = kubeirsa.main:main'
            ]
        },
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
 )