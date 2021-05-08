#!/usr/bin/env python
"""
Config a file
-------------

If 'TARGET' doesn't exist, the file will be unchanged, and
you will be notified

Usage:

python3 omni_config.py FILE "{"TARGET": "NEW_VALUE", "SOME_OTHER_TARGET:": 42}"

"""

import os, sys, ast, re



FILE = "/home/irreq/github/config/tests/alacritty.yml"
FILE = 'myfile.txt'
n_changes = 0

rules = {
    "TERM:": "xterm-256color_new_lol",
}

def find_and_replace(target, result, lst):
    return [line.replace(target, result) for line in lst]

def find_and_replace_word_after(target, result, string):
    enc = string
    # enc = enc.split()
    # enc = [i for j in enc.split() for i in (j, ' ')][:-1]
    # enc = re.split(r'(\s+)', enc)
    # enc = re.split(r"(\s+)", enc)

    # enc = '{"cyan:": "'"0x06989a"'"}'
    enc = re.split(r"(\s+)", enc)
    # enc = re.split(r"/[^a-zA-Z ]+/ig", enc)
    # enc = re.split(r"(?U)(?<=\\s)(?=\\S)|(?<=\\S)(?=\\s)", enc)
    loge = enc

    old_res = result

    # print(result)
    #
    # print(loge)
    # exit()

    position = 0
    found = False
    for i, item in enumerate(enc):
        if item == target:
            found = True
            position = i
            break

    if len(enc) == position + 1:
        if not found:
            return string

    if not found:  # Usually what happens
        return string

    try:
        enc[position+2] = result
    except IndexError:
        print("We are now force-adding variables that did not exist earlier")
        enc.append(result)

    global n_changes
    n_changes += 1
    print(string)


    result = "".join([str(i) for i in enc])
    print(result)
    print(loge)
    print(old_res)

    # if result==string:
    #     print("Nothing have changed")

    return result

def old_main():
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

def string_to_dict(string):
    try:
        return ast.literal_eval(string)
    except Exception as e:
        print(e)
        return {}


def main(content, rules):
    tmp = content.copy()
    for key in rules:
        tmp = [find_and_replace_word_after(key, rules[key], i) for i in tmp]

    if tmp != content:
        print("Applying changes...")
    return tmp




def test():
    # Python program to
    # demonstrate readline()

    L = ["Geeks aa\n", "for\n", "Geeks\n"]

    # Writing to a file
    file1 = open('myfile.txt', 'w')
    file1.writelines((L))
    file1.close()

    # Using readline()
    file1 = open('myfile.txt', 'r')
    count = 0

    while True:
        count += 1
        line = file1.readline()
        if not line:
            break
        print("{} {}".format(count, line.strip()))

    file1.close()


if __name__ == "__main__":
    # test()
    # exit()

    if len(sys.argv) != 4:
        print(__doc__)
        exit(0)

    if sys.argv[2] == "-rules":
        rules = string_to_dict(sys.argv[3])

    elif sys.argv[2] == "-file":
        if not os.path.isfile(sys.argv[3]):
            print("No such file found")
            exit(0)

        with open(sys.argv[3], "r") as f:
            """
            File must look similar to this:

            rules = {
                "bg": "#0000ff"
            }

            """
            res = f.readlines()
            string = " ".join([i.strip() for i in res])
            string = string.split("{")[1]
            string = string.split("}")[0]
            string = "{"+string+"}"
            f.close()

        rules = string_to_dict(string)


    else:
        print(__doc__)
        exit(0)

    if not os.path.isfile(sys.argv[1]):
        print("No such file found")
        exit(0)

    tmp = []
    count = 0
    print(rules)

    with open(sys.argv[1], "r") as f:
        while True:
            count += 1
            line = f.readline()
            if not line:
                break

            for key in rules:
                new_line = find_and_replace_word_after(key, rules[key], line)
                if new_line != line:
                    line = new_line
                    break
            tmp.append(line)
        f.close()

    with open(sys.argv[1], "w") as f:
        for i in tmp:
            f.write(i)
        f.close()

    print("Config file has now been modified!")
