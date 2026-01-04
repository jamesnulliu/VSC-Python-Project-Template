from pathlib import Path
import sys
import subprocess
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext

""" You may want to change the following variables to customize your project """
# Root directory:
ROOT_DIR = Path(__file__).parent
# Name of your package; Must match the directory name under `CSRC_DIR`:
PKG_NAME = "simple_py"
# Path to the directory of setup.py file:
SETUP_DIR = Path(__file__).parent.absolute()
# Where to create the cmake build directory:
BUILD_DIR = Path(SETUP_DIR, "build")
# Path to the c/c++ source directory:
CSRC_DIR = Path(SETUP_DIR, "csrc")
# Name of the extended C library module:
LIB_NAME = "extended_clib"
"""''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''"""


class CMakeExtension(Extension):
    def __init__(
        self, name, source_dir, build_dir, build_args: list[str] = None
    ):
        """
        CMake extension for setuptools.

        Arguments
        ---------
        name : str
            Name of the extension.
        source_dir : str | Path
            Path to the C/C++ source directory.
        build_dir : str | Path
            Path to the build directory.
        build_args : list[str], optional
            Additional build arguments for CMake.
            Check `csrc/scripts/build.sh` for usage.
        """
        Extension.__init__(self, name, sources=[])
        self.source_dir = Path(source_dir).absolute()
        self.build_dir = Path(build_dir).absolute()
        self.build_args = ["Release"] if build_args is None else build_args


class CMakeBuild(build_ext):
    def run(self):
        try:
            subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError("CMake must be installed")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext: CMakeExtension):
        ext_install_dir = (
            Path(self.get_ext_fullpath(ext.name)).parent / LIB_NAME
        )
        build_args = ["-S", ext.source_dir,
                      "-B", ext.build_dir]  # fmt: skip
        build_args += ext.build_args
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
            ext_install_dir,
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
            name=f"{PKG_NAME}.extended_clib",
            source_dir=CSRC_DIR,
            build_dir=BUILD_DIR,
            build_args=None,
        )
    ],
    cmdclass={"build_ext": CMakeBuild},
    packages=find_packages(where="./src"),
    package_dir={PKG_NAME: f"./src/{PKG_NAME}"},
    install_requires=get_requirements(ROOT_DIR),
)
