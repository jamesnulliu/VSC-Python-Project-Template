import inspect
import importlib.util
import sys
import re
from pathlib import Path


def detect_module_name(lib_path: Path) -> str:
    """
    Scans the binary file to find the PyInit_<name> symbol.
    """
    with open(lib_path, "rb") as f:
        content = f.read()

    # We look for the byte pattern 'PyInit_' followed by alphanumeric characters
    # This covers the standard C export symbol for Python 3 modules.
    match = re.search(b"PyInit_([a-zA-Z0-9_]+)", content)

    if not match:
        raise ValueError(
            f"Could not find a PyInit_ export in {lib_path}."
            + "Is this a valid Python extension?"
        )

    # Decode bytes to string (e.g., b'example_cpp' -> 'example_cpp')
    return match.group(1).decode("utf-8")


def import_extended_clib(lib_path: str, module_name: str = None):
    caller_frame = inspect.stack()[1]
    caller_module = inspect.getmodule(caller_frame[0])
    caller_dir = Path(caller_frame.filename).parent.resolve()

    if caller_module is None:
        raise ImportError("Could not determine the calling package.")

    target_path = Path(lib_path)
    if not target_path.is_absolute():
        target_path = (caller_dir / target_path).resolve()

    if not target_path.exists():
        raise FileNotFoundError(f"Shared library not found at: {target_path}")

    if module_name is None:
        try:
            module_name = detect_module_name(target_path)
            print(f"Auto-detected module name: {module_name}")
        except Exception as e:
            raise ImportError(f"Failed to detect module name from binary: {e}")

    full_name = f"{caller_module.__name__}.{module_name}"

    spec = importlib.util.spec_from_file_location(full_name, str(target_path))
    if spec is None:
        raise ImportError(f"Could not load spec from {target_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[full_name] = module
    spec.loader.exec_module(module)

    setattr(caller_module, module_name, module)

    return module
