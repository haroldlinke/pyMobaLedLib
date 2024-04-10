"""Base classes for all plug-ins"""

import os
import re
import imp
from .utils import rootPath
from .config import VB2PYConfig
from . import logger

Config = VB2PYConfig()
log = logger.getLogger("PlugInLoader")


# << Plug-in functions >> (1 of 2)
def loadAllPlugins():
    """Load all plug-ins from the plug-in directory and return a list of all the classes"""
    from . import plugins
    mods = []
    for mod in plugins.mods:
        log.debug("Checking '%s' for plugins" % mod)
        #
        filename = os.path.join(rootPath(), "plugins", "%s.py" % mod)
        f = open(filename, "r")
        try:
            try:
                m = imp.load_module(mod, f, filename, ('*.py', 'r', 1))
            finally:
                f.close()
        except Exception as err:
            log.warn("Error importing '%s' (%s). Module skipped" % (mod, err))
            continue
        #
        for name in dir(m):
            cls = getattr(m, name)
            # import pdb; pdb.set_trace()
            try:
                is_plugin = cls.__is_plugin__
            except AttributeError:
                is_plugin = 0
            if is_plugin:
                try:
                    p = cls()
                    log.debug("Added new plug-in: '%s" % p.name)
                    mods.append(p)
                except Exception as err:
                    log.warn("Error creating plugin '%s' (%s). Class skipped" % (cls, err))
    #
    # Now sort
    mods.sort(key=lambda plugin: plugin.order)
    return mods


def disableLogging():
    """Disable logging in all plugins"""
    #
    # Disable the main logger
    log.setLevel(0)
    #
    # Now do so for pluging
    BasePlugin.logging_level = 0


class BasePlugin(object):
    """All plug-ins should inherit from this base class or define __is_plugin__"""

    __is_plugin__ = 1  # Set to true if you want to be loaded plug-in

    system_plugin = 0  # True if you are a system plugin
    __enabled = 1  # If false the plugin will not be called
    order = 1000  # Determines order of execution. lower = earlier

    logging_level = int(Config["General", "LoggingLevel"])

    def __init__(self):
        """Initialize the plugin

        This method should always be called by subclasses as it is required to set up logging etc

        """
        if not hasattr(self, "name"):
            self.name = self.__class__.__name__

        self.log = logger.getLogger(self.name)
        self.log.setLevel(self.logging_level)

    def preProcessVBText(self, text):
        """Process raw VB text prior to any conversion

        This method should return a new version of the text with any changes made
        to it. If there is no preprocessing required then do not define this method.

        """
        return text

    def postProcessPythonText(self, text):
        """Process Python text following the conversion

        This method should return a new version of the text with any changes made
        to it. If there is no postprocessing required then do not define this method.

        """
        return text

    def disable(self):
        """Disable the plugin"""
        self.__enabled = 0

    def isEnabled(self):
        """Return 1 if plugin is enabled"""
        return self.__enabled

    def __cmp__(self, other):
        """Used to allow plugins to be sorted to run in a certain order"""
        return cmp(self.order, other.order)


class RETextMarkup(BasePlugin):
    """A utility class to apply regular expression based text markup

    The plug-in allows simple re text replacements as a pre and post conversion
    passes simple by reading from lists of replacements defined as class methods.

    Users can simply create instances of their own classes to handle whatever markup
    they desire.

    """

    name = "RETextMarkup"
    re_flags = 0  # Put re flags here if you need them

    # Define your patterns by assigning to these properties in the sub-class
    pre_process_patterns = ()
    post_process_patterns = ()

    def preProcessVBText(self, text):
        """Process raw VB text prior to any conversion"""
        if self.pre_process_patterns:
            self.log.info("Processing pre patterns")
        return self.processText(text, self.pre_process_patterns)

    def postProcessPythonText(self, text):
        """Process Python text following the conversion"""
        if self.post_process_patterns:
            self.log.info("Processing post patterns")
        return self.processText(text, self.post_process_patterns)

    def processText(self, text, patterns):
        """Process the text and mark it up"""
        for re_pattern, replace in patterns:
            def doSub(match):
                self.log.info("Replacing '%s' with %s, %s" % (re_pattern, replace, match.groupdict()))
                return replace % match.groupdict()

            r = re.compile(re_pattern, self.re_flags)
            text = r.sub(doSub, text)
        return text


class RenderHookPlugin(BasePlugin):
    """A utility plugin to hook a render method and apply markup after the render

    The plugin replaces the specified objects normal renderCode method with one which
    calls the plugins addMarkup method when it is complete.

    """

    name = "RenderHookPlugin"
    hooked_class_name = None  # Name of class should go here

    def __init__(self):
        """Initialize the plugin

        This method should always be called by subclasses as it is required to set up logging etc

        """
        super(RenderHookPlugin, self).__init__()
        #
        # Look for class and replace its renderAsCode method
        from . import parserclasses
        self.hooked_class = getattr(parserclasses, self.hooked_class_name)
        old_render_method = self.hooked_class.renderAsCode

        #
        def newRender(obj, indent=0):
            ret = old_render_method(obj, indent)
            return self.addMarkup(indent, ret)

        #
        self.hooked_class.renderAsCode = newRender

    def addMarkup(self, indent, text):
        """Add markup to the rendered text"""
        return text


class SystemPlugin(BasePlugin):
    """Special kind of plug-in which is used by the system and cannot be disabled"""

    system_plugin = 1


class SystemPluginREPlugin(RETextMarkup):
    """Special kind of plug-in which is used by the system and cannot be disabled"""

    system_plugin = 1


if __name__ == "__main__":
    loadAllPlugins()
