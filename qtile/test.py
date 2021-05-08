import os
import sys
arg = r"flatpak run io.atom.Atom"
arg = r"flatpak run com.microsoft.Teams"

# os.system(arg)

# with open("/home/irreq/github/config/qtile/log.txt", "w") as f:
#     f.write(" ".join(sys.argv[1:]))
#     f.close()
os.system(" ".join(sys.argv[1:]))
