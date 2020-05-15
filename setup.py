import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyowapi",
    version="1.1.0",
    author="Tobias Messner",
    author_email="tobias.d.messner@gmail.com",
    description="An asynchronous wrapper for ow-api.com using aiohttp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZusorCode/pyowapi",
    packages=setuptools.find_packages(),
    install_requires=["aiohttp"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    test_suite='nose.collector',
    tests_require=['nose'],
)
