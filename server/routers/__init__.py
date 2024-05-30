import os
from .Store import store

from .utils import *

from .log import createlog
from .Api import Api
from .Use import use

log = createlog('\\'.join(__file__.split("\\")[:-2]))