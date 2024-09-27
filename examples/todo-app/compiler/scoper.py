import re
import hashlib
import logging

logger = logging.getLogger(__name__)

class ComponentScoper:
    def generate_component_id(self, component_name):
        return hashlib.md5(component_name.encode()).hexdigest()[:8]

    def adjust_template_scoping(self, template, component_id):
        # Recursively update IDs and class names in the template
        for elem in template.iter():
            if 'id' in elem.attrib:
                elem.attrib['id'] = f"{elem.attrib['id']}_{component_id}"
            if 'class' in elem.attrib:
                classes = elem.attrib['class'].split()
                classes = [f"{cls}_{component_id}" for cls in classes]
                elem.attrib['class'] = ' '.join(classes)

    def adjust_script_scoping(self, script, component_id):
        if script.text:
            # Prefix function and variable names for unique scoping
            pattern = r'\b(function\s+|var\s+|let\s+|const\s+)(\w+)'
            replacement = rf'\1\2_{component_id}'
            script.text = re.sub(pattern, replacement, script.text)
            # Adjust DOM selectors
            script.text = script.text.replace('document.getElementById(', f'getElementById_component(')
            script.text = script.text.replace('document.querySelector(', f'querySelector_component(')

    def adjust_style_scoping(self, style, component_id):
        if style.text:
            # Prefix class and ID selectors in the styles
            style.text = re.sub(r'(\.|#)(\w+)', rf'\1\2_{component_id}', style.text)
