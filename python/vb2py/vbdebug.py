"""Set up logging"""

from . import vbclasses
import logging

from . import logger   # For logging output and debugging 
#_vb_debug_log = logger.getLogger("vb2PyApp")

_vb_debug_log = logging.getLogger("vb2PyApp")

vbclasses.Debug._logger = _vb_debug_log

#logger=logging.getLogger(__name__)

#vbclasses.Debug._logger = logger