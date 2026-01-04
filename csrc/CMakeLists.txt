# Minimum required CMake version
cmake_minimum_required(VERSION 3.30)

# Project Name and version
project(SIMPLE_PY VERSION 1.0.0)

# Common utility functions
include(${PROJECT_SOURCE_DIR}/cmake/utils/common.cmake)

# @see "./cmake/utils/variables.cmake"
set_default_values(
    # CMake project namespace:
    #   All the libs should have a alias with this namespace
    PROJECT_NAMESPACE "simple_py::"
    STDOUT_IS_TERMINAL OFF
    CMAKE_EXECUTABLE_SUFFIX ""
)

# Utility functions for installing libraries:
include(${PROJECT_SOURCE_DIR}/cmake/utils/lib-install.cmake)

# Compiler configurations for cpp, e.g., g++, clang++, msvc(cl), etc.
include(${PROJECT_SOURCE_DIR}/cmake/compilers/cxx-compiler-configs.cmake)
# Compiler configurations for CUDA:
include(${PROJECT_SOURCE_DIR}/cmake/compilers/cuda-compiler-configs.cmake)

# Find other libraries:
include(${PROJECT_SOURCE_DIR}/cmake/libraries/libpython.cmake)
include(${PROJECT_SOURCE_DIR}/cmake/libraries/libtorch.cmake)
include(${PROJECT_SOURCE_DIR}/cmake/libraries/libpybind11.cmake)

add_subdirectory(${PROJECT_SOURCE_DIR}/lib)
add_subdirectory(${PROJECT_SOURCE_DIR}/test)