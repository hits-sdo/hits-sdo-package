import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="hits-sdo-packager",
    version="0.1.0",
    author="NASA 2023 HITS-SDO team",
    # author_email="subhamoy",
    description="Tile and augment SDO images",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/hits-sdo/hits-sdo-packager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)