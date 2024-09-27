# parser.py
import xml.etree.ElementTree as ET
import sys
import logging

logger = logging.getLogger(__name__)

class JTMLParser:
    def parse_jtml_file(self, file_path):
        logger.debug(f"Parsing JTML file: {file_path}")
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            logger.info(f"Successfully parsed '{file_path}'")
            return root
        except ET.ParseError as e:
            logger.error(f"Error parsing '{file_path}': {e}")
            sys.exit(1)
        except FileNotFoundError:
            logger.error(f"File not found: '{file_path}'")
            sys.exit(1)
        except Exception as e:
            logger.error(f"An unexpected error occurred while parsing '{file_path}': {e}")
            sys.exit(1)

    def validate_component(self, root, file_path):
        if root.tag != 'component':
            logger.error(f"Error in '{file_path}': Root element must be <component>")
            sys.exit(1)
        required_children = {'template', 'script', 'style'}
        present_children = {child.tag for child in root}
        missing_children = required_children - present_children
        if missing_children:
            logger.error(f"Error in '{file_path}': Missing required sections: {', '.join(missing_children)}")
            sys.exit(1)
