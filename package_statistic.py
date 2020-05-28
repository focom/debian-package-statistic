#!/usr/bin/env python3
import gzip
import os
import sys
import tempfile

import requests

AVAILABLES_ARCH = [
    "amd64",
    "arm64",
    "armel",
    "armhf",
    "i386",
    "mips",
    "mips64el",
    "mipsel",
    "ppc64el",
    "s390x",
]

DEBIAN_FTP_URL = "http://ftp.uk.debian.org/debian/dists/stable/main/"


def parse_arch(args):
    if len(args) == 1:
        print("Please pass a arch as a parameter")
        sys.exit(1)
    if len(args) > 2:
        print("Too many argument")
        sys.exit(1)
    if args[1] not in AVAILABLES_ARCH:
        print(f"{args[1]} is not a recognized arch")
        sys.exit(1)
    return args[1]


def download_file(download_dir, arch):
    file_url = DEBIAN_FTP_URL + "Contents-" + arch + ".gz"
    local_filename = os.path.join(download_dir, file_url.split("/")[-1])

    with requests.get(file_url, stream=True) as stream:
        stream.raise_for_status()
        with open(local_filename, "wb") as gzip_file:
            for chunk in stream.iter_content(chunk_size=8192):
                gzip_file.write(chunk)
    return local_filename


def print_top_10_packages(package_count):
    sorted_packages = sorted(package_count, key=package_count.__getitem__, reverse=True)

    i = 0
    for package in sorted_packages:
        i += 1
        if i > 10:
            break
        print(f"{i}. {package}\t{package_count[package]}")


def process_content_file(content_file):
    package_count = {}

    for line in content_file:
        match_result = str(line).split(" ")[-1]
        packages = match_result.replace("\\n", "").replace("'", "").split(",")
        for package in packages:
            package = package.split("/")[1]
            try:
                package_count[package] += 1
            except KeyError:
                package_count[package] = 1
    return package_count


def main():
    with tempfile.TemporaryDirectory() as tempdir:
        arch = parse_arch(sys.argv)
        gzip_filename = download_file(tempdir, arch)

        with gzip.open(gzip_filename, "r") as content_file:
            package_count = process_content_file(content_file)

        print_top_10_packages(package_count)
        sys.exit(0)


if __name__ == "__main__":
    main()
