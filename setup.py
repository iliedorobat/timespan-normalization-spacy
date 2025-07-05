from setuptools import setup, find_packages

setup(
    name="temporal_normalization_spacy",
    version="2.0.1",
    author="Ilie Cristian Dorobat",
    description="A spaCy plugin for identifying and parsing historical data "
                "in Romanian texts",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iliedorobat/timespan-normalization-spacy",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "temporal_normalization.libs": ["temporal-normalization-2.0.jar"],
    },
    install_requires=["spacy>=3.0", "py4j", "langdetect"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
