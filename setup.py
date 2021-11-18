import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="python-commandmaker",
    version="0.0.5",
    author="Cube Riser",
    author_email="cuberiser@gmail.com",
    long_description_content_type="text/markdown",
    long_description=str(long_description),
    description="Python module for discord bot like commands from the console",
    python_requires=">=3.10.0",
    packages=setuptools.find_packages(),
    install_requires=[""],
)
