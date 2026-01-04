#include <pybind11/pybind11.h>
#include <string>
#include <utility>

namespace py = pybind11;

// --- 1. A Simple C++ Function ---
auto add(int i, int j) -> int
{
    return i + j;
}

// --- 2. A Simple C++ Class ---
class Pet
{
public:
    Pet(std::string name) : m_name(std::move(name))
    {
    }

    void setName(const std::string& name)
    {
        m_name = name;
    }

    [[nodiscard]] auto getName() const -> const std::string&
    {
        return m_name;
    }

    [[nodiscard]] auto greet() const -> std::string
    {
        return "Woof! My name is " + m_name;
    }

    std::string m_name;
};

// --- 3. The Binding Code ---
// "extended_clib" is the name of the module we will import in Python
PYBIND11_MODULE(extended_clib, m)
{
    // Bind the function
    m.def("add", &add, "A function that adds two numbers");

    // Bind the Pet class
    py::class_<Pet>(m, "Pet")
        .def(py::init<const std::string&>())   // Constructor
        .def("setName", &Pet::setName)         // Setter
        .def("getName", &Pet::getName)         // Getter
        .def("greet", &Pet::greet)             // Method
        .def_readwrite("name", &Pet::m_name);  // Public member variable
}