# example_plugin.py
from compiler.plugin_interface import CompilerPlugin
import logging

logger = logging.getLogger(__name__)

class ExamplePlugin(CompilerPlugin):
    def process_script(self, script):
        if script.text:
            # Example: Add a console log at the beginning of each script
            script.text = 'console.log("Script executed");\n' + script.text
            logger.debug("ExamplePlugin: Added console log to script")
