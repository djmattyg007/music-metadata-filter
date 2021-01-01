import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="music-metadata-filter", # Replace with your own username
    version="1.0.0",
    author="Matthew Gamble",
    author_email="git@matthewgamble.net",
    description="A module for cleaning up artist, album, and song names.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/djmattyg007/music-metadata-filter",
    packages=setuptools.find_packages(include=("music_metadata_filter",)),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
    ],
    python_requires='>=3.7',
)
