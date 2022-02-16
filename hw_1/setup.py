import setuptools
from setuptools import setup

setup(
    name="fib_list_ast",
    version="1.0",
    author="Filippov Denis",
    author_email="fild10@yandex.ru",
    url="https://github.com/DF5HSE/AdvancedPython2022",
    install_requires=[
        "networkx==2.5.1",
        "pydot==1.4.2",
        "graphviz==0.19.1",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
) 
