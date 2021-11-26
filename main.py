#!/usr/bin/env python3

import argparse

from server import FileService


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", default='files', type=str, help="Path to file, root by default")
    args = parser.parse_args()

    FileService.change_dir(args.d)


if __name__ == "__main__":
    main()
