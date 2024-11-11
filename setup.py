import sys
import os
from os import path as osp
import subprocess
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    def __init__(self, name, source_dir, build_dir, install_dir):
        Extension.__init__(self, name, sources=[])
        self.source_dir = osp.abspath(source_dir)
        self.build_dir = osp.abspath(build_dir)
        self.install_dir = osp.abspath(install_dir)


class CMakeBuild(build_ext):

    def run(self):
        try:
            subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError("CMake must be installed")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext: CMakeExtension):
        build_args = [
            "-S",
            ext.source_dir,
            "-B",
            ext.build_dir,
            "Release",
        ]
        # If Current Platform is Windows
        if sys.platform == "win32":
            subprocess.check_call([r"csrc\scripts\build.bat"] + build_args)
        else:
            subprocess.check_call(["bash", "csrc/scripts/build.sh"] + build_args)
        install_args = [
            "--install",
            ext.build_dir,
            "--prefix",
            ext.install_dir,
        ]
        subprocess.check_call(["cmake"] + install_args)


ABS_SETUP_DIR = osp.dirname(osp.abspath(__file__))
BUILD_DIR = osp.join(ABS_SETUP_DIR, "build")
CSRC_DIR = osp.join(ABS_SETUP_DIR, "csrc")
PACKAGE_DIR = osp.join(ABS_SETUP_DIR, "example_package")

setup(
    ext_modules=[
        CMakeExtension(
            name="example_package._torch_ops_cxx",
            source_dir=CSRC_DIR,
            build_dir=BUILD_DIR,
            install_dir=osp.join(PACKAGE_DIR, "_torch_ops_cxx"),
        )
    ],
    cmdclass={"build_ext": CMakeBuild},
    packages=find_packages(),
    package_data={
        "example_package": ["_torch_ops_cxx/lib/*.so", "_torch_ops_cxx/lib/*.pyd"]
    },
)
