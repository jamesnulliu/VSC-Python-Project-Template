include(${CMAKE_CURRENT_LIST_DIR}/../utils/logging.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/../utils/run-python.cmake)

set(PY_RESULT)
set(PY_OUTPUT)
set(PY_ERROR)

# 1. Run Python to get the pybind11 CMake directory
run_python(
    "import pybind11; print(pybind11.get_cmake_dir())"
    PY_RESULT PY_OUTPUT PY_ERROR
)

# 2. Add the result to the CMAKE_PREFIX_PATH
# PY_OUTPUT will look something like: .../site-packages/pybind11/share/cmake/pybind11
list(APPEND CMAKE_PREFIX_PATH "${PY_OUTPUT}")

# 3. Now CMake can find it standardly
find_package(pybind11 REQUIRED)