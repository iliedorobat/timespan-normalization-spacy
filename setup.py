from setuptools import setup, find_packages

setup(
    name="temporal_normalization_spacy",
    version="2.2.1",
    author="Ilie Cristian Dorobat",
    description="A spaCy plugin for temporal normalization and extraction of "
    "historical dates in Romanian narrative texts.",
    keywords="spacy, nlp, temporal normalization, timex, historical dates, romanian",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iliedorobat/timespan-normalization-spacy",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "spacy_factories": [
            "temporal_normalization=temporal_normalization_spacy.factory:create_component",
        ],
    },
    package_data={
        "temporal_normalization.libs": ["temporal-normalization-2.1.0.jar"],
    },
    install_requires=[
        "spacy>=3.8.7,<4.0.0",
        "py4j>=0.10.9.9",
        "langdetect>=1.0.9"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9,<3.13",
)
