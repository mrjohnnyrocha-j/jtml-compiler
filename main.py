# main.py
import logging
import argparse
import configparser
from compiler.compiler import JTMLCompiler

def main():
    parser = argparse.ArgumentParser(description='JTML Compiler')
    parser.add_argument('files', nargs='+', help='JTML files to compile')
    parser.add_argument('--no-minify', action='store_true', help='Disable minification')
    parser.add_argument('--log-level', default='INFO', help='Set logging level')
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('compiler.log'),
        ]
    )

    compiler = JTMLCompiler(minify=not args.no_minify)
    compiler.compile(args.files)

if __name__ == '__main__':
    main()
