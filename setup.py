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

setup_info = dict(
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

setup(**setup_info)
