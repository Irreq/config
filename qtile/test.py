prgs = {"test":"abc",
        "foo": "lol",
        "list": ["nice", "cool"],
        "notlist": "tru"
        }


lst = list(prgs.keys())

def filtering_function(filter, lst):
    return [k for k in lst if filter in k]

print(lst)
li = "li"
a = filtering_function(li, lst)
print(a)
