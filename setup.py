"""
Setup script for Purepy.

This file is kept for compatibility, but the main configuration
is now in pyproject.toml following modern Python packaging standards.
"""

from setuptools import setup

# Read the contents of README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="purepy",
    version="1.0.0",
    author="YonLD",
    author_email="istintin@outlook.com",
    description="A Python templating engine inspired by ReactJS functional components",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YonLD/purepy",
    packages=["pure", "pure.core"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Text Processing :: Markup :: XML",
    ],
    python_requires=">=3.8",
    keywords="html xml svg templating template-engine web frontend component react",
    project_urls={
        "Bug Tracker": "https://github.com/YonLD/purepy/issues",
        "Documentation": "https://github.com/YonLD/purepy#readme",
        "Source Code": "https://github.com/YonLD/purepy",
    },
)
