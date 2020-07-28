#!/usr/bin/env python3

import click
import json
from bs4 import BeautifulSoup
from html.parser import HTMLParser


@click.command()
@click.argument("src", nargs=1, type=click.Path(exists=True))
@click.argument("dst", nargs=1, type=click.Path())
def main(src, dst):
    """
    Transform the HTML code of https://www.fixtrading.org/extension-packs/
    into a set of links for each Extension Pack.
    """
    links = {}
    with open(src, "r") as f:
        soup = BeautifulSoup(f.read(), "lxml")
    tags = soup.findAll("a", {"class": "wpdm-download-link"})
    for tag in tags:
        container = tag.parent.parent
        title = container.find("div", {"class": "media-body"}).find("h3")
        ep = title.find("a").getText().split(" ")[0][2:]
        if not ep:
            ep = title.find("a").getText().split(" ")[1]
        links[ep] = tag["onclick"].split("'")[1]
    with open(dst, "w") as f:
        json.dump(links, f, indent=2)
    print("-- Transformed HTML page to JSON links.")


if __name__ == "__main__":
    main()
