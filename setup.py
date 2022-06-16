"""
-- Created by Pravesh Budhathoki
-- Treeleaf Technologies Pvt. Ltd.
-- Created on 2022-06-15
"""
import re
import sys
from setuptools import find_packages, setup

TORCH_AVAILABLE = True
try:
    import torch
    from torch.utils import cpp_extension
except ImportError:
    TORCH_AVAILABLE = False
    print("[WARNING] Unable to import torch, pre-compiling ops will be disabled.")


def get_package_dir():
    pkg_dir = {
        "yolox.tools": "tools",
        "yolox.exp.default": "exps/default",
    }
    return pkg_dir


def get_install_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        reqs = [x.strip() for x in f.read().splitlines()]
    reqs = [x for x in reqs if not x.startswith("#")]
    return reqs


def get_yolox_version():
    with open("yolox/__init__.py", "r") as f:
        version = re.search(
            r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
            f.read(), re.MULTILINE
        ).group(1)
    return version


def get_long_description():
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
    return long_description


def get_ext_modules():
    ext_module = []
    if sys.platform != "win32":  # pre-compile ops on linux
        assert TORCH_AVAILABLE, "torch is required for pre-compiling ops, please install it first."
        # if any other op is added, please also add it here
        from yolox.layers import FastCOCOEvalOp
        ext_module.append(FastCOCOEvalOp().build_op())
    return ext_module


def get_cmd_class():
    cmdclass = {}
    if TORCH_AVAILABLE:
        cmdclass["build_ext"] = cpp_extension.BuildExtension
    return cmdclass


setup(
    name="yolox",
    version="1.0",
    author="Pravesh Kaji Budhathoki",
    url="https://github.com/Megvii-BaseDetection/YOLOX",
    package_dir=get_package_dir(),
    packages=find_packages(exclude=("tests", "tools")) + list(get_package_dir().keys()),
    python_requires=">=3.6",  # avoid building error when pip is not updated
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    include_package_data=True,  # include files in MANIFEST.in
    classifiers=[
        "Programming Language :: Python :: 3", "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
    ],
    project_urls={
        "Documentation": "https://yolox.readthedocs.io",
        "Source": "https://github.com/Megvii-BaseDetection/YOLOX",
        "Tracker": "https://github.com/Megvii-BaseDetection/YOLOX/issues",
    },
)
