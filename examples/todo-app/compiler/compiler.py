# compiler.py
from .parser import JTMLParser
from .scoper import ComponentScoper
from .bundler import ModuleBundler
from .minifier import Minifier
from .dependency_resolver import DependencyResolver
from .plugin_interface import CompilerPlugin
import logging
import xml.etree.ElementTree as ET
import importlib
import pkgutil

logger = logging.getLogger(__name__)

class JTMLCompiler:
    def __init__(self, minify=True):
        self.parser = JTMLParser()
        self.scoper = ComponentScoper()
        self.bundler = ModuleBundler()
        self.minifier = Minifier()
        self.dependency_resolver = DependencyResolver()
        self.minify = minify
        self.plugins = self.load_plugins()


    def load_plugins(self):
        plugins = []
        for finder, name, ispkg in pkgutil.iter_modules(['plugins']):
            module = importlib.import_module(f'plugins.{name}')
            for attr in dir(module):
                cls = getattr(module, attr)
                if isinstance(cls, type) and issubclass(cls, CompilerPlugin) and cls != CompilerPlugin:
                    plugins.append(cls())
                    logger.debug(f"Loaded plugin: {cls.__name__}")
        return plugins

    def compile(self, file_paths):
        components = {}
        for file_path in file_paths:
            root = self.parser.parse_jtml_file(file_path)
            self.parser.validate_component(root, file_path)
            component_name = root.attrib.get('name')
            component_id = self.scoper.generate_component_id(component_name)
            dependencies = self.dependency_resolver.parse_dependencies(root)
            components[component_name] = {
                'root': root,
                'id': component_id,
                'dependencies': dependencies,
                'file_path': file_path
            }

        dependency_graph = self.dependency_resolver.build_dependency_graph(components)
        sorted_components = self.dependency_resolver.topological_sort(dependency_graph)

        templates = []
        scripts = []
        styles = []

        for component_name in sorted_components:
            component = components[component_name]
            root = component['root']
            component_id = component['id']
            template = self.extract_and_scope_component(root, 'template', component_id)
            script = self.extract_and_scope_component(root, 'script', component_id)
            style = self.extract_and_scope_component(root, 'style', component_id)
            if template is not None:
                templates.append(template)
            if script is not None:
                scripts.append(script)
            if style is not None:
                styles.append(style)

        # Consolidate templates, scripts, and styles
        html_content = self.consolidate_templates(templates)
        js_content = self.bundler.bundle_modules(scripts)
        js_content = self.minifier.minify_js(js_content, self.minify)
        css_content = self.minifier.minify_css(self.consolidate_styles(styles), self.minify)

        # Combine everything into a string to return
        output = f'''<!DOCTYPE html>
        <html>
        <head>
            <title>JTML Application</title>
            <link rel="stylesheet" href="styles.css">
        </head>
        <body>
        {html_content}
        <script src="app.js"></script>
        </body>
        </html>
        '''

        # Return the full HTML content
        return output


    def extract_and_scope_component(self, root, component_name, component_id):
        for child in root:
            if child.tag == component_name:
                if component_name == 'template':
                    self.scoper.adjust_template_scoping(child, component_id)
                elif component_name == 'script':
                    self.scoper.adjust_script_scoping(child, component_id)
                    self.wrap_script_in_module(child, component_id)
                elif component_name == 'style':
                    self.scoper.adjust_style_scoping(child, component_id)
                return child
        return None

    def wrap_script_in_module(self, script, component_id):
        if script.text:
            module_code = f'''
// Module for component {component_id}
export function component_{component_id}() {{
{script.text}
}}
'''
            script.text = module_code

    def consolidate_templates(self, templates):
        html_content = ''
        for template in templates:
            content = ''.join(ET.tostring(e, encoding='unicode', method='html') for e in template)
            html_content += content + '\n'
        return html_content

    def consolidate_styles(self, styles):
        css_content = ''
        for style in styles:
            css_content += style.text or ''
            css_content += '\n'
        return css_content

    def write_output_files(self, html_content, js_content, css_content):
        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(f'''<!DOCTYPE html>
                <html>
                <head>
                    <title>JTML Application</title>
                    <link rel="stylesheet" href="styles.css">
                </head>
                <body>
                {html_content}
                <script src="app.js"></script>
                </body>
                </html>
                ''')
        with open('app.js', 'w', encoding='utf-8') as file:
            file.write(js_content)
        with open('styles.css', 'w', encoding='utf-8') as file:
            file.write(css_content)
        logger.info("Compilation successful. Files generated: index.html, app.js, styles.css")

    def progressive_compile(self, file_paths, stage='intermediate'):
        """
        Perform progressive compilation.
        Stages can be: 'intermediate', 'final'.
        """
        if stage == 'intermediate':
            # Extract an intermediate representation of components
            intermediate_components = self.compile_to_intermediate(file_paths)
            logger.info("Intermediate compilation complete.")
            return intermediate_components
        elif stage == 'final':
            # Do a full compilation in the final stage
            logger.info("Final compilation initiated.")
            return self.compile(file_paths)
        else:
            raise ValueError(f"Unknown compilation stage: {stage}")

    def compile_to_intermediate(self, file_paths):
        """
        Extract an intermediate representation (IR) for progressive compilation.
        """
        components = {}
        for file_path in file_paths:
            root = self.parser.parse_jtml_file(file_path)
            self.parser.validate_component(root, file_path)
            component_name = root.attrib.get('name')
            component_id = self.scoper.generate_component_id(component_name)
            components[component_name] = {
                'root': root,
                'id': component_id,
                'file_path': file_path
            }

        # Return some form of intermediate representation (could be abstract or partially parsed)
        return components
    
    