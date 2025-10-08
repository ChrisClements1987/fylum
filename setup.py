from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fylum",
    version="1.0.0",
    author="Chris Clements",
    author_email="",
    description="A smart file organizer CLI tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChrisClements1987/fylum",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "typer>=0.9.0",
        "pydantic>=2.0.0",
        "PyYAML>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "fylum=app:app",
        ],
    },
)
