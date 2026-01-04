#include <torch/extension.h>
#include <torch/library.h>

#include "simple_py/math/vec_add.hpp"

auto vector_add(const torch::Tensor& A, const torch::Tensor& B) -> torch::Tensor
{
    auto N = A.size(0);
    auto C = torch::empty_like(A);

    // If A and B both on CUDA
    if (A.is_cuda() && B.is_cuda()) {
        simple_py::cuda::launch_vec_add(
            A.data_ptr<float>(), B.data_ptr<float>(), C.data_ptr<float>(), N);
    } else if (A.is_cpu() && B.is_cpu()) {
        simple_py::cpu::launch_vec_add(A.data_ptr<float>(), B.data_ptr<float>(),
                                       C.data_ptr<float>(), N);
    } else {
        AT_ERROR("Not implemented for CPU and CUDA");
    }
    return C;
}

// Define operator `torch.ops.simple_py.vector_add`.
// @see
// "https://docs.google.com/document/d/1_W62p8WJOQQUzPsJYa7s701JXt0qf2OfLub2sbkHOaU/edit?tab=t.0#heading=h.fu2gkc7w0nrc"
TORCH_LIBRARY(simple_py, m)
{
    m.def("vector_add(Tensor a, Tensor b) -> Tensor");
}

// Register the implementation.
// @see
// "https://docs.google.com/document/d/1_W62p8WJOQQUzPsJYa7s701JXt0qf2OfLub2sbkHOaU/edit?tab=t.0#heading=h.jc288bcufw9a"
TORCH_LIBRARY_IMPL(simple_py, CPU, m)
{
    m.impl("vector_add", &::vector_add);
}
TORCH_LIBRARY_IMPL(simple_py, CUDA, m)
{
    m.impl("vector_add", &::vector_add);
}