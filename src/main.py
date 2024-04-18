import os
import shutil
from htmlnode import markdown_to_blocks, markdown_to_html_node

# path to static assets
static = 'static/'


# moves static assets from provided dir to public dir
def move_static(dir):
    for node in os.listdir(dir):
        path = os.path.join(dir, node)
        if os.path.isfile(path):
            os.makedirs(dir.replace('static/', 'public/'))
            shutil.copy(path, path.replace('static/', 'public/'))
        else:
            move_static(path)


# extracts the first header from provided md
def extract_title(md):
    blocks = markdown_to_blocks(md)
    for block in blocks:
        if block.startswith('# '):
            return block.replace('# ', '')
    raise Exception("All pages need a single h1 header")


# generates an html page from md content and a template
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # the markdown
    md = open(from_path).read()
    # the html template
    template = open(template_path).read()
    # the html parent div to be injected into template
    html = markdown_to_html_node(md).to_html()
    # the title of the page
    title = extract_title(md)
    # the full page html
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    # the path to the page excluding the file
    dirs = '/'.join(dest_path.split('/')[:-1])
    # makes the dirs for the file if they don't exist yet
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    # write full page html to the destination html file
    with open(dest_path, 'w') as dest:
        dest.write(page)
        dest.close()


# parses through provided root directory to generate pages off any mds found
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for node in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, node)
        # generate a page when a file is found
        if os.path.isfile(path):
            generate_page(path, template_path, os.path.join(dest_dir_path, node).replace('.md', '.html'))
        # parse through next dir if no file found
        else:
            generate_pages_recursive(path, template_path, os.path.join(dest_dir_path, node))


def main():
    # removes the public dir so it can be built
    shutil.rmtree('public/')
    # copies static assets 
    move_static(static)
    # generates pages from the content directory
    generate_pages_recursive('content/', 'template.html', 'public/')
    return 


main()