import os
import re, mmap

files = {
    "alacritty": "/home/irreq/github/config/tests/alacritty.yml",
}





def read_search_in_file(file):
    with open(file, 'r+') as f:
        data = mmap.mmap(f.fileno(), 0).read().decode("utf-8")
        error = re.search(r'error: (.*)', data)
  if error:
    return error.group(1)


def find_and_replace(target, result, lst):
    return [line.replace(target, result) for line in lst]

def find_and_replace_word_after(target, result, string):
    enc = string
    enc = enc.split()
    position = 0
    found = False
    for i, item in enumerate(enc):
        print(item)
        if item == target:
            found = True
            position = i
            break

    if len(enc) == position + 1:
        print("Nothing was found for this query")
        return string

    if not found:
        print("Fucjk")
        return string

    enc[position+1] = result

    return " ".join(enc)

class Files():
    def __init__(self):
        pass

    def alacritty(self, content):
        changes = {
        "Configuration for Alacritty, the": "Lol fuckoff",
        "draw_bold_text_with_bright_colors: true": "draw_bold_text_with_bright_colors: false",


        }
        words = content.copy()

        words[0] = find_and_replace_word_after("Alacritty,", "Nice ass bro...", words[0])

        for item in changes:
            words = find_and_replace(item, changes[item], words)


        # words[0] = "Fuck"
        # words = [word.replace('WinPTY backend (Windows only)','<br />') for word in words]
        print("yay it worked!")
        print(content==words)
        print(content[:20])
        print(words[:20])


def main():
    files_functions = Files()

    for file in files:
        print(file)
        try:
            path = files[file]
            if os.path.isfile(path):
                with open(path, "r") as f:
                    content = f.readlines()
                    f.close()
                result = getattr(files_functions, file)(content)
        except Exception:
            pass



if __name__ == "__main__":
    main()
