from setuptools import setup, find_packages

setup(
    name="My_Suncsreen",
    version="0.1.0",
    description="Premium Sunscreen Launch Strategy — data-driven market analysis for India",
    author="Aditya Jhajhra",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.26.0",
        "pandas>=2.0.0",
        "streamlit>=1.30.0",
        "scikit-learn>=1.3.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
)