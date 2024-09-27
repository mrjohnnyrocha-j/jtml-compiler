# bundler.py
import logging

logger = logging.getLogger(__name__)

class ModuleBundler:
    def bundle_modules(self, scripts):
        js_content = ''
        module_exports = []
        for script in scripts:
            js_content += script.text or ''
            js_content += '\n'
            match = re.search(r'export function (\w+)', script.text or '')
            if match:
                module_exports.append(match.group(1))
        js_content += '\n// Initialize modules\n'
        for export in module_exports:
            js_content += f'{export}();\n'
        return js_content
