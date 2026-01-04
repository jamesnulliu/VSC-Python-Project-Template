#include <cstdint>
#include <cstdio>

#include "simple_py/math/vec_add.hpp"
#include "simple_py/utils/address.hpp"

namespace simple_py::cpu
{

void launch_vec_add(const float* a, const float* b, float* c, int n)
{
    ::printf("Hello World from CPU!\n");
    ::printf("Vector size: %d\n", n);

    for (int i = 0; i < n; ++i) {
        auto offset = computeOffset<std::size_t>(1, 2, 3, 4, 5, 6);
        ::printf("Offset: %d\n", std::uint32_t(offset));
        c[i] = a[i] + b[i];
    }
}

}  // namespace simple_py::cpu
