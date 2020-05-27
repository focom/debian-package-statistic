#!/usr/bin/env python3
import gzip
import os
import sys
import tempfile
from pathlib import Path

# install request with: pip install requests
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
    if len(args) > 2:
        print("Too many argument")
        sys.exit()
    if args[1] not in AVAILABLES_ARCH:
        print(f"{args[1]} is not a recognized arch")
        sys.exit()
    return args[1]


def download_file(download_dir, arch):
    file_url = DEBIAN_FTP_URL + "Contents-" + arch + ".gz"
    local_filename = os.path.join(download_dir, file_url.split("/")[-1])
    # NOTE the stream=True parameter below
    with requests.get(file_url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def print_top_10_packages(package_count):
    sorted_packages = sorted(package_count, key=package_count.__getitem__, reverse=True)

    i = 0
    for package in sorted_packages:
        i += 1
        if i > 10:
            break
        print(f"{i}. {package}\t{package_count[package]}")


def main():
    with tempfile.TemporaryDirectory() as tempdir:
        arch = parse_arch(sys.argv)
        gzip_filename = download_file(tempdir, arch)

        content_filepath = os.path.join(tempdir, "content_file.txt")
        Path(content_filepath).touch()

        package_count = {}

        with gzip.open(gzip_filename, "r") as f:
            for line in f:
                match_result = str(line).split(' ')[-1]
                packages = match_result.replace("\\n", "").replace("'","").split(",")
                for package in packages:
                    package = package.split('/')[1]
                    try:
                        package_count[package] += 1
                    except KeyError:
                        package_count[package] = 1

        print_top_10_packages(package_count)


if __name__ == "__main__":
    main()
