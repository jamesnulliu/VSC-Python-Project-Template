# VSC-Python-Project-Template
A Template of Python Project in Visual Studio Code with Github Actions CI/CD (Especially for PyTorch based Deeplearning Projects).

## How to Build

```bash
conda create -n pytemplate python=3.12
conda activate pytemplate
pip install .
```

`torch.ops.example_package.vector_add` will be available after installation.

## How to Test

```bash
conda activate pytemplate
python test/test.py
```