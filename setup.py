from setuptools import setup, find_packages

setup(
    name="stock-analysis-tool",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'pandas',
        'requests',
    ],
)