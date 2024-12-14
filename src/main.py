import os
import shutil

from textnode import TextNode, TextType

def main() -> int:
    cp_dir("static", "public")
    return 0

def cp_dir(original: str, dest: str) -> None:
    # Find current files in destination directory and remove them
    if os.path.exists(dest):
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


main()
