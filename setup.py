from setuptools import setup, find_packages
from os import path
from io import open
import glob

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, "fix2dict", "__version__.py"), encoding="utf-8") as f:
    version = {}
    exec(f.read(), version)
    VERSION = version["__version__"]

with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

RESOURCES = list(
    glob.iglob(path.join(HERE, "fix2dict", "resources/**/*"), recursive=True)
)

setup(
    name="fix2dict",
    version=VERSION,
    description="FIX Dictionary generator tool",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/fixipe/fix2dict",
    author="Filippo Costa @neysofu",
    author_email="filippocosta.italy@gmail.com",
    license="Apache Software License",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="FIX protocol XML fintech finance trading",
    packages=find_packages(),
    package_data={"fix2dict": RESOURCES},
    python_requires=">=3.5",
    install_requires=[
        "nltk==3.4.5",
        "click",
        "natsort==7.0.1",
        "checksumdir==1.1.7",
        "setuptools>=41",
        "dict-recursive-update==1.0.1",
        "jsonpatch==1.25",
        "jsonschema==3.2.0",
    ],
    entry_points="""
    [console_scripts]
    fix2dict=fix2dict.cli:cli
    """,
    test_suite="nose.collector",
    tests_require=["nose"],
)
