from rjsmin import jsmin
from csscompressor import compress
import logging

logger = logging.getLogger(__name__)

class Minifier:
    def minify_js(self, js_content, minify=True):
        if minify:
            logger.debug("Minifying JavaScript content")
            return jsmin(js_content)
        return js_content

    def minify_css(self, css_content, minify=True):
        if minify:
            logger.debug("Minifying CSS content")
            return compress(css_content)
        return css_content
