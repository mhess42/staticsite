import os
import shutil
from htmlnode import markdown_to_blocks, markdown_to_html_node

static = 'static/'
def move_static(dir):
    for node in os.listdir(dir):
        path = os.path.join(dir, node)
        if os.path.isfile(path):
            os.makedirs(dir.replace('static/', 'public/'))
            shutil.copy(path, path.replace('static/', 'public/'))
        else:
            move_static(path)


def extract_title(md):
    blocks = markdown_to_blocks(md)
    for block in blocks:
        if block.startswith('# '):
            return block.replace('# ', '')
    raise Exception("All pages need a single h1 header")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = open(from_path).read()
    template = open(template_path).read()
    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    # os.makedirs('/'.join(dest_path.split('/')[:-1]))
    with open(dest_path, 'w') as dest:
        dest.write(page)
        dest.close()

def main():
    move_static(static)
    generate_page('content/index.md', 'template.html', 'public/index.html')
    return 

main()