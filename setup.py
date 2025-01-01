from setuptools import setup, find_packages

setup(
    name="mcap-profiles",
    version="0.1.0",
    author="Abdel YEZZA",
    author_email="abdel.yezza24@gmail.com",  
    description="Un package pour l'affectation des profils aux activités",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ayezza/profiles_assignment", 
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "scikit-learn"
    ],
    entry_points={
        'console_scripts': [
            'mcap=main:main',
        ],
    },
    include_package_data=True,
    package_data={
        'mcap_profiles': ['data/input/*.csv', 'config/*.ini'],
    },
) 