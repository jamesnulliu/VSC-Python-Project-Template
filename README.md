# VSC-Python-Project-Template
A Template of Python Project in Visual Studio Code with Github Actions CI/CD (Especially for PyTorch based Deeplearning Projects).

## How to Build

Create a new conda environment:

```bash
$ uv venv -p 3.12
$ source .venv/bin/activate
```

Install `simple_py`:

```bash
$ uv install -v .
```

`torch.ops.simple_py.vector_add` will be available after installation; See [test.py](test/test.py) for usage.

## How to Test

```bash
python test/test.py
```