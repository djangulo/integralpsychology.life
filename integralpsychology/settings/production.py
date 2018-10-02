from .base import *
from integralpsychology.secrets import SECRET_KEY

DEBUG = False

try:
    from .local import *
except ImportError:
    pass
