from setuptools import setup, find_packages
import io

# Read README with explicit UTF-8 encoding
with io.open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mcap-processor",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.26.4",
        "pandas>=2.2.1",
        "scikit-learn>=1.3.2",
        "matplotlib>=3.8.2",
        "fastapi>=0.115.8",
        "uvicorn>=0.34.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for MCAP matrix processing and profile assignments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="mcap, matrix, profile assignment",
    python_requires=">=3.8",
)