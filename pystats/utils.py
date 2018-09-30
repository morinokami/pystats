import re
import yaml


def is_text(file_data):
    threshold = 0.3
    text_chars = bytearray(range(32,127)) + bytearray(b'\b\f\n\r\t')

    data_length = len(file_data)
    if not data_length:
        return True

    if b'\x00' in file_data:
        return False

    binary_length = len(file_data.translate(None, delete=text_chars))
    return binary_length / data_length < threshold

def is_inline_comment(line):
    pat = rb'^\s*#[^\n]*'
    match = re.search(pat, line)
    return match is not None

def extract_block_comments(data):
    pat = rb'^\s*([\'"])\1\1(.*?)\1{3}'
    matches = re.findall(pat, data, re.DOTALL | re.MULTILINE)
    return [m[1] for m in matches]

def extract_functions(data):
    import ast
    tree = ast.parse(data)
    nodes = ast.walk(tree)
    return [node for node in nodes if type(node) == ast.FunctionDef]

def get_languages(filename):
    res = []

    with open('pystats/data/languages.yml') as f:
        languages = yaml.load(f)
        for lang in languages:
            filenames = languages[lang]['filenames']
            extensions = languages[lang]['extensions']
            for suffix in filenames + extensions:
                if filename.endswith(suffix):
                    res.append(lang)
        
        return res
