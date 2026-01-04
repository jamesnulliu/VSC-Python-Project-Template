set(LIB_NAME "ExtendedPet")

Python_add_library(${LIB_NAME} SHARED pet.cpp)
add_library(${PROJECT_NAMESPACE}${LIB_NAME} ALIAS ${LIB_NAME})

target_link_libraries(
    ${LIB_NAME} 
    PUBLIC 
    pybind11::module
)

# @see "cmake/utils/lib-install.cmake"
install_libraries(${LIB_NAME} ${PROJECT_NAMESPACE} ${LIB_NAME})