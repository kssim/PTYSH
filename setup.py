#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

packages = ["ptysh", "modules", "daemon_example"]

requires = [
    "python-config",
    "dbus-python"
]

with open("README.md") as f:
    readme = f.read()

with open("VERSION") as f:
    version = f.read()

setup(
    name = "ptysh",
    version = version,
    description = "Python Teletype Shell",
    long_description = readme,
    author = "kssim",
    author_email = "ksub0912@gmail.com",
    url = "https://github.com/kssim/PTYSH",
    packages = packages,
    packages_data = {},
    package_dir = {},
    include_package_data = True,
    install_requires = requires,
    setup_requires = [],
    tests_require = [],
    license = "MIT License",
    zip_safe = False,
    scripts = ["bin/ptysh"],
    keywords=["shell", "cli", "tty", "terminal", "python cli", "python tty"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: System Shells",
        "Topic :: System :: Shells",
        "Topic :: Terminals",
        "Topic :: Utilities",
    ],
)
