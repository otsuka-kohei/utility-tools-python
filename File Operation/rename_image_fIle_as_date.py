# python3

import sys
import os
import glob
import datetime
import zlib


def main():
    args = sys.argv

    if len(args) < 2:
        print("arg error: please set dir path")
        return

    path = args[1]
    path = complete_path(path)

    keyword = ""
    if len(args) > 2:
        keyword = args[2]

    file_paths = glob.glob(path + "*" + keyword + "*")
    for file_path in file_paths:
        time = os.path.getmtime(file_path)
        time = datetime.datetime.fromtimestamp(time)
        time = time.strftime("%Y%m%d_%H%M%S")

        hash = get_crc32_from_path(file_path)

        suffix = get_suffix(file_path)
        new_file_path = path + "IMG_" + time + "_" + hash + "." + suffix

        if os.path.isfile(new_file_path):
            print("ignore " + file_path)
            continue
        else:
            print("rename " + file_path + " to " + new_file_path)
            os.rename(file_path, new_file_path)


def complete_path(arg_path):
    splited_dir = arg_path.split(os.sep)
    if splited_dir[-1] != "":
        return arg_path + os.sep
    else:
        return arg_path


def get_suffix(path):
    splited_dir = path.split(os.sep)
    filename = splited_dir[-1]
    splited_file_name = filename.split(".")
    if len(splited_file_name) > 1:
        return splited_file_name[-1]
    else:
        return ""


def get_crc32_from_path(file_path):
    data = open(file_path, "rb")
    byte_array = data.read()
    hash = zlib.crc32(byte_array)
    hash = hex(hash)
    hash = hash.split("x")
    hash = hash[1]
    return hash


if __name__ == "__main__":
    main()