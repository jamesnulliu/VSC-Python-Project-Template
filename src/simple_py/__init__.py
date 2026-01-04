import torch
from pathlib import Path
from .utils.clib_importer import import_extended_clib

PACKAGE_DIR = Path(__file__).resolve().parent
print(PACKAGE_DIR)


# [SEE] "https://docs.google.com/document/d/1_W62p8WJOQQUzPsJYa7s701JXt0qf2OfLub2sbkHOaU/edit?tab=t.0#heading=h.i5q3a2pv0qzc"
torch.ops.load_library(
    PACKAGE_DIR / "extended_clib/lib/libExtendedTorchOps.so"
)

import_extended_clib(PACKAGE_DIR / "extended_clib/lib/libExtendedPet.so")
