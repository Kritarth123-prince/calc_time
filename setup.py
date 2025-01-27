from setuptools import setup, find_packages

setup(
    name="calc_time",
    version="1.0.0",
    author="Kritarth",
    author_email="kritarthranjan.iitb@gmail.com",
    description="A package to calculate the total duration of audio and video files in a directory.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kritarthranjan123-prince/calc_time",
    packages=find_packages(),
    install_requires=[
        "mutagen",
        "moviepy"
    ],
    entry_points={
        "console_scripts": [
            "calc_time=calc_time.calc_time:main",
        ],
    },
    python_requires=">=3.9",
)