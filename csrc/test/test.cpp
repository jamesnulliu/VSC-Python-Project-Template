#include <simple_py/math/vec_add.hpp>
#include <vector>

auto main() -> int
{
    std::vector<float> a(100);
    std::vector<float> b(100);
    std::vector<float> c(100);

    simple_py::cpu::launch_vec_add(a.data(), b.data(), c.data(), 100);
    simple_py::cuda::launch_vec_add(a.data(), b.data(), c.data(), 100);

    return 0;
}