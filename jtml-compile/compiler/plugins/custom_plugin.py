# plugins/custom_plugin.py
from compiler.plugin_interface import CompilerPlugin

class CustomPlugin(CompilerPlugin):
    def process_script(self, script):
        # Custom processing
        pass
