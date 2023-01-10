"""
 setup.py
 
 EPCC, The University of Edinburgh
 
 (c) 2023 The University of Edinburgh
 
 Contributing Authors:
 Christodoulos Stylianou (c.stylianou@ed.ac.uk)
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
 	http://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Parse version number from sparse_tree/__init__.py:
with open("sparse_tree/__init__.py") as f:
    info = {}
    for line in f:
        if line.startswith("__version__"):
            exec(line, info)
            break

setup(
    name="sparse_tree",
    version=info["__version__"],
    author="Christodoulos Stylianou",
    author_email="c.stylianou@ed.ac.uk",
    url="https://github.com/morpheus-org/sparse.tree",
    description="Sparse Matrix Format Selection using Decision Trees",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    # Package info
    packages=["sparse_tree"],
    install_requires=["scikit-learn", "ssgetpy", "pandas", "numpy", "matplotlib"],
)
