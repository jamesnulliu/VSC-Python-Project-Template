#include "project-name/system.hpp"
#include <cstdint>

namespace project_namespace::cuda
{
VSC_CPP_TEMPLATE_API void launch_vec_add(const float* const a,
                                         const float* const b, float* const c,
                                         const int n);
}

namespace project_namespace::cpu
{
VSC_CPP_TEMPLATE_API void launch_vec_add(const float* const a,
                                         const float* const b, float* const c,
                                         const int n);
}
