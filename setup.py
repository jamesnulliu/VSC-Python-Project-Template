from pathlib import Path
import sys
import subprocess
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext

""" You may want to change the following variables to customize your project """
# Root directory:
ROOT_DIR = Path(__file__).parent
# Name of your package; Must match the directory name under `CSRC_DIR`:
PKG_NAME = "example_package"
# Path to the directory of setup.py file:
SETUP_DIR = Path(__file__).parent.absolute()
# Where to create the cmake build directory:
BUILD_DIR = Path(SETUP_DIR, "build")
# Path to the c/c++ source directory:
CSRC_DIR = Path(SETUP_DIR, "csrc")
# Where to install the op library:
TORCH_OPS_DIR = Path(SETUP_DIR, "src", PKG_NAME, "_torch_ops")
"""''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''"""


class CMakeExtension(Extension):
    def __init__(self, name, source_dir, build_dir, install_dir):
        Extension.__init__(self, name, sources=[])
        # C/C++ source directory
        self.source_dir = Path(source_dir).absolute()
        # Build directory
        self.build_dir = Path(build_dir).absolute()
        # Lib installation directory
        self.install_dir = Path(install_dir).absolute()


class CMakeBuild(build_ext):
    def run(self):
        try:
            subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError("CMake must be installed")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext: CMakeExtension):
        build_args = ["-S", ext.source_dir,
                      "-B", ext.build_dir,
                      "Release"]  # fmt: skip
        # If Current Platform is Windows
        if sys.platform == "win32":
            subprocess.check_call(
                [R"csrc\scripts\msvc-bash.bat", R"csrc\scripts\build.sh"]
                + build_args
            )
        else:
            subprocess.check_call(
                ["bash", "csrc/scripts/build.sh"] + build_args
            )
        install_args = [
            "--install",
            ext.build_dir,
            "--prefix",
            ext.install_dir,
        ]
        subprocess.check_call(["cmake"] + install_args)


def get_requirements(root_dir: Path) -> list[str]:
    """Get Python package dependencies from requirements.txt."""
    requirements_dir = root_dir / "requirements"

    def _read_requirements(filename: str) -> list[str]:
        with open(requirements_dir / filename) as f:
            requirements = f.read().strip().split("\n")
        resolved_requirements = []
        for line in requirements:
            if line.startswith("-r "):
                resolved_requirements += _read_requirements(line.split()[1])
            elif (
                not line.startswith("--")
                and not line.startswith("#")
                and line.strip() != ""
            ):
                resolved_requirements.append(line)
        return resolved_requirements

    requirements = _read_requirements("common.txt")
    return requirements


setup(
    ext_modules=[
        CMakeExtension(
            name=f"{PKG_NAME}._torch_ops",
            source_dir=CSRC_DIR,
            build_dir=BUILD_DIR,
            install_dir=TORCH_OPS_DIR,
        )
    ],
    cmdclass={"build_ext": CMakeBuild},
    packages=find_packages(where="./src"),
    package_dir={PKG_NAME: "./src"},
    package_data={
        # Use relative path here
        PKG_NAME: ["_torch_ops/lib/*.so", "_torch_ops/lib/*.dll"]
    },
    install_requires=get_requirements(ROOT_DIR),
)
