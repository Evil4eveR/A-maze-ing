from setuptools import setup, find_packages

setup(
    name="mazegen",
    version="1.0.0",
    description="Reusable maze generator",
    python_requires=">=3.10",
    packages=find_packages(where=".", include=["mazegen", "mazegen.*"]),
)
