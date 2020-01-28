from .version import __version__
from .shout import shout_and_repeat
from .add import my_add
from .compute_duration import compute_duration, store_result
# if somebody does "from somepackage import *", this is what they will
# be able to access:
__all__ = [
    'shout_and_repeat',
    'my_add',
    'compute_duration',
    'store_result',
]
