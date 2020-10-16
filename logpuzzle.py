#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

__author__ = "Larry Scott, Pete Mayor, and students"
"""
import os
import re
import sys
import urllib.request
import argparse

def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    with open (filename, 'r') as f:
        data = f.read()
        print(data)
        my_domain = "http://" + filename.split("_")[1]
        image = re.findall(r"(?<=\"GET )(.*?)(?=.jpg)", data)
        image_url = []
        for img in image:
            url = f'{my_domain}{img}.jpg'
            image_url.append(url)
        print(image_url)
        image_url_set = set(image_url)
        image_url_list = list(image_url_set)
        image_url_list.sort(key=lambda x: x[-8:-4])
        
        return image_url_list
    pass


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    if not (os.path.isdir(dest_dir)):
        os.makedirs(dest_dir)

    for i, img in enumerate(img_urls):
        img_path = os.path.join(dest_dir, "img" + str(i) + ".jpg")
        print(img)
        if img.find("no_picture") == -1:   
            urllib.request.urlretrieve(img, img_path)

    
    with open(os.path.join(dest_dir, "index.html"), "w") as f:
        f.write("<html><body>")
        for i, img in enumerate(img_urls[:-1]):
            f.write(f"<img src='img{i}.jpg'>")
        f.write("</body></html>")

    


    pass


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
