class CompilerPlugin:
    def process_template(self, template):
        """Hook to process the template before it's compiled."""
        pass

    def process_script(self, script):
        """Hook to process the script before it's compiled."""
        pass

    def process_style(self, style):
        """Hook to process the style before it's compiled."""
        pass
