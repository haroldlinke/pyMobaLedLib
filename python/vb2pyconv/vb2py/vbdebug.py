"""Set up logging"""

from . import vbclasses

from . import logger   # For logging output and debugging 
_vb_debug_log = logger.getLogger("vb2PyApp")

vbclasses.Debug._logger = _vb_debug_log
