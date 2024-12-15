import os
from os.path import isdir, isfile
import shutil

from textnode import TextNode, TextType
from util import (extract_title,
                  markdown_to_html_node)

def main() -> int:
    """
    copy static files to public directory, then generate all html pages
    from the markdown files in the `content` directory.
    """
    cp_dir("static", "public")
    # Generate an html page from markdown
    generate_pages_recursive("content", "template.html", "public")
    return 0

def cp_dir(original: str, dest: str) -> None:
    if os.path.exists(dest):
        # Find current files in destination directory and remove them
        old_files: list = os.listdir(dest)
        for filename in old_files:
            if os.path.isfile(os.path.join(dest, filename)):
                os.remove(os.path.join(dest, filename))
            else:
                shutil.rmtree(os.path.join(dest, filename))
    # Find files in original directory and copy them to destination
    static_files: list = os.listdir(original)
    for filename in static_files:
        o_path: str = os.path.join(original, filename)
        d_path: str = os.path.join(dest, filename)
        if os.path.isfile(o_path):
            shutil.copy(o_path, d_path)
        else:
            os.mkdir(d_path)
            # recurse as needed
            cp_dir(o_path, d_path)
    return

def generate_page(original_path, template_path, dest_path) -> None:
    print(f"Generating page from {original_path} to {dest_path} using {template_path}...")
    original: str = open(original_path).read()
    template: str = open(template_path).read()
    title: str = extract_title(original)
    content: str = markdown_to_html_node(original).to_html()
    html: str = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    os.makedirs(dest_path[:dest_path.rindex('/')], exist_ok=True)
    open(dest_path, 'w').write(html)
    return

def generate_pages_recursive(original_dir, template_path, target_dir) -> None:
    print(f"Generating pages from {original_dir} to {target_dir} using {template_path}...")
    original: list = os.listdir(original_dir)
    for path in original:
        o_path: str = os.path.join(original_dir, path)
        if path[-3:] == '.md':
            d_path: str = os.path.join(target_dir, path[:-3] + ".html")
        else:
            d_path: str = os.path.join(target_dir, path)
        if os.path.isfile(o_path):
            generate_page(o_path, template_path, d_path)
        elif os.path.isdir(o_path):
            os.makedirs(d_path)
            generate_pages_recursive(o_path, template_path, d_path)
        else:
            pass
    return


main()
