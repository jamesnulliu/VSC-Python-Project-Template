#include "simple_py/system.hpp"

namespace simple_py::cuda
{
SIMPLE_PY_API void launch_vec_add(const float* a, const float* b,
                                            float* c, int n);
}

namespace simple_py::cpu
{
SIMPLE_PY_API void launch_vec_add(const float* a, const float* b,
                                            float* c, int n);
}
