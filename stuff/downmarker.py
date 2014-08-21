#!/home1/chanspac/python3/bin/python3.2
"""Usage: downmarker.py CONFIGFILE"""
import configparser
import markdown
import os.path
import sys

INPUT_ENCODING = 'utf-8'
OUTPUT_ENCODING = 'utf-8'

header_printed = False

def write_output(s=None, *, code=None):
    global header_printed
    if not header_printed:
        if code:
            sys.stdout.buffer.write(code.encode(OUTPUT_ENCODING) + b"\n")
        else:
            sys.stdout.buffer.write(b"Content-type: text/html; charset=utf-8"
                                    b"\n\n")
        header_printed = True
    if s:
        sys.stdout.buffer.write(s.encode(OUTPUT_ENCODING))

try:
    input_file = sys.argv[1]
except IndexError:
    write_output("Provide a page config file as an argument!")
    sys.exit(0)

if not os.path.isfile(input_file):
    write_output(code="Status: 404 Not Found")
    sys.exit(0)

# Find default.ini
path = os.path.dirname(input_file)
while not os.path.isfile(os.path.join(path, 'default.ini')):
    oldpath, path = path, os.path.dirname(path)
    if path == oldpath:
        write_output(code="Status: 500 Internal Server Error")
        write_output("I couldn't find default.ini anywhere!")
        sys.exit(0)

config_files = [os.path.join(path, 'default.ini'), input_file]
config = configparser.ConfigParser()
loaded_files = config.read(config_files, INPUT_ENCODING)
if len(loaded_files) < 2:
    write_output(code="Status: 500 Internal Server Error")
    write_output("I couldn't load one of the config files!")
    sys.exit(0)

# Load the header and footer
header_file = os.path.join(path, config['Page']['header'])
footer_file = os.path.join(path, config['Page']['footer'])
header = open(header_file, encoding=INPUT_ENCODING).read()
footer = open(footer_file, encoding=INPUT_ENCODING).read()
header = header.format(**config['Page'])
footer = footer.format(**config['Page'])

# Load the body
body_file = os.path.join(path, config['Page']['body'])
body = open(body_file, encoding=INPUT_ENCODING).read()
body = markdown.markdown(body, extensions=['codehilite'],
                         output_format='html5')

# Print everything
write_output(header)
write_output(body)
write_output(footer)
sys.exit(0)
