import torch
import simple_py
from simple_py.utils.logging_config import init_loggers
import logging


init_loggers("configs/loggers.yml")


A = torch.tensor([1, 2, 3], dtype=torch.float32)
B = torch.tensor([4, 5, 6], dtype=torch.float32)

pet = simple_py.extended_clib.Pet("Kitty")
logging.info(pet.greet())

logger = logging.getLogger("DEBUG")
logger.debug(torch.ops.simple_py.vector_add(A, B))

A = A.cuda()
B = B.cuda()

logger.debug(torch.ops.simple_py.vector_add(A, B))
