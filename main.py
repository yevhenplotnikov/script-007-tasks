#!/usr/bin/env python3

import argparse

from server.FileService import change_dir, get_files


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", default='/work/files', type=str, help="Path to file, root by default")
    args = parser.parse_args()

    change_dir(args.d)
    print(get_files())

    pass


if __name__ == "__main__":
    main()
