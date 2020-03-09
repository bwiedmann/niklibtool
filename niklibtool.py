#!/usr/bin/python

import os, sys, io

TARGET_DIR = "/Library/Application Support/Native Instruments/Service Center"

def register_library(file_path):
    name = file_path.split(os.sep)[-1].split(".")[0]
    print("Registering {0}...".format(name))

    content = io.BytesIO()
    
    lib_file = open(file_path, "rb")
    lib_file.seek(256)
    
    while True:
        c = lib_file.read(1)
        if c == chr(0):
            break

        content.write(c)
    
    lib_file.close()

    out_path = os.path.join(TARGET_DIR, name + ".xml")
    with open(out_path, "wb") as hints_file:
        hints_file.write(content.getvalue())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    else:
        print("Please provide a path to scan.")
        sys.exit()

    if not os.path.exists(base_dir):
        print("Provided path does not exist.")
        sys.exit()

    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith(".nicnt") and not f.startswith("."):
                register_library(os.path.join(root, f))
    
    print("Done.")
