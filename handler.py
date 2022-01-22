import argparse
import hashlib
import os
from collections import defaultdict


def get_path():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=False)
    args = parser.parse_args()
    if args.path:
        return args.path


def get_files(path: str, form: str):
    lst = defaultdict(list)
    for root, dirs, files in os.walk(path):
        for i in files:
            if i.endswith(form):
                path = os.path.join(root, i)
                size = os.stat(path).st_size
                lst[size].append(path)
    for k in tuple(lst.keys()):
        if len(lst[k]) < 2:
            del lst[k]
    return lst


def choice_sorting():
    print("Size sorting options:\n1. Descending\n2. Ascending\n")
    srt = input("Enter a sorting option:\n")
    while srt not in ("1", "2"):
        print("\nWrong option\n")
        srt = input("Enter a sorting option:\n")
    return False if srt == "2" else True


def print_files(lst: defaultdict, srt: bool):
    srt_keys = sorted(lst, reverse=srt)
    for i in srt_keys:
        print()
        print(i, "bytes")
        for f in lst[i]:
            print(f)


def ask_yes_no(question: str):
    rep = input(f"\n{question}\n")
    while rep.lower() not in ("y", "yes", "n", "no"):
        print("\nWrong option\n")
        rep = input(f"{question}\n")
    return 0 if rep in ("n", "no") else 1


def check_hashes(files: list):
    hashes_dict = {}
    for file in files:
        with open(file, "rb") as f:
            file_content = f.read()
        hash_file = hashlib.md5(file_content).hexdigest()
        if not hashes_dict.get(hash_file):
            hashes_dict.update({hash_file: [file]})
        else:
            hashes_dict[hash_file].append(file)
    for k in tuple(hashes_dict.keys()):
        if len(hashes_dict[k]) < 2:
            del hashes_dict[k]
    return hashes_dict


def get_duplicates(lst: defaultdict, srt: bool):
    duplicates = {}
    srt_sizes = sorted(lst.keys(), reverse=srt)
    for size in srt_sizes:
        hashes_dict = check_hashes(lst[size])
        if hashes_dict and hashes_dict.items():
            duplicates[size] = hashes_dict
    return duplicates


def print_files_duplicates(duplicates: dict):
    count = 1
    for size, hashes_dict in duplicates.items():
        if hashes_dict and hashes_dict.items():
            print()
            print(size, "bytes")
            for hsh, dup in hashes_dict.items():
                print(f"Hash: {hsh}")
                for path in dup:
                    print(f"{count}. {path}")
                    count += 1


def get_duplicates_paths(duplicates: dict):
    paths = {}
    count = 0
    for size, d in duplicates.items():
        for p in d.values():
            for path in p:
                paths[count] = (path, size)
                count += 1
    return paths


def ask_files_numbers(count: int):
    numbers = [str(i + 1) for i in range(count)]
    rep = input("\nEnter file numbers to delete:\n").split()
    while True:
        if rep:
            for i in rep:
                if i not in numbers:
                    break
            else:
                return tuple(int(x) - 1 for x in set(rep))
        print("\nWrong option\n")
        rep = input("Enter file numbers to delete:\n").split()


def delete_files(paths: dict, numbers: tuple):
    mem = 0
    for numb in paths:
        if numb in numbers:
            os.remove(paths[numb][0])
            mem += paths[numb][1]
    print(f"\nTotal freed up space: {mem} bytes")


def main():
    path = get_path()
    if not path:
        return print("Directory is not specified")
    form = input("Enter file format:\n")
    srt = choice_sorting()
    lst = get_files(path, form)
    print_files(lst, srt)
    if ask_yes_no("Check for duplicates?"):
        duplicates = get_duplicates(lst, srt)
        print_files_duplicates(duplicates)
        if ask_yes_no("Delete files?"):
            paths = get_duplicates_paths(duplicates)
            files_numbers = ask_files_numbers(len(paths.keys()))
            delete_files(paths, files_numbers)


if __name__ == "__main__":
    main()
