import os
import shutil

from textnode import TextNode, TextType
from util import (extract_title,
                  markdown_to_html_node)

def main() -> int:
    # copy static files to public directory
    cp_dir("static", "public")
    # Generate an html page from markdown
    generate_page("content/index.md", "template.html", "public/index.html")
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
        o_file: str = os.path.join(original, filename)
        d_file: str = os.path.join(dest, filename)
        if os.path.isfile(o_file):
            shutil.copy(o_file, d_file)
        else:
            os.mkdir(d_file)
            # recurse as needed
            cp_dir(o_file, d_file)
    return

def generate_page(original_path, template_path, dest_path) -> None:
    print(f"Generating page from {original_path} to {dest_path} using {template_path}")
    original: str = open(original_path).read()
    template: str = open(template_path).read()
    title: str = extract_title(original)
    content: str = markdown_to_html_node(original).to_html()
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    os.makedirs(dest_path[:dest_path.rindex('/')], exist_ok=True)
    open(dest_path, 'w').write(html)
    return


main()
