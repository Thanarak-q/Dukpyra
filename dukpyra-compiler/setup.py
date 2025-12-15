from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="dukpyra",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Python to ASP.NET Core Compiler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dukpyra",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "ply>=3.11",
        "watchdog>=3.0.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "dukpyra=dukpyra.cli:main",
        ],
    },
    include_package_data=True,
)
