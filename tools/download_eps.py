#!/usr/bin/env python3

import click
import requests
import json
import shutil
import time
import zipfile
import os


@click.command()
@click.argument("links", nargs=1, type=click.Path(exists=True))
@click.argument("dst", nargs=1, type=click.Path(exists=True))
@click.argument("headers", nargs=1, type=click.Path(exists=True))
@click.option("--download-again", default=False, type=click.BOOL)
def main(links, dst, headers, download_again):
    """
    Download Expansion Pack data from a set of links <LINKS>.
    """
    # Read input JSON.
    with open(links) as f:
        links = json.load(f)
    with open(headers) as f:
        headers = json.load(f)
    for (ep, url) in links.items():
        dir = os.path.join(dst, "EP" + str(ep))
        if os.path.exists(dir):
            if download_again:
                shutil.rmtree(dir)
            else:
                print("-- EP{}.xml found, not downloading again".format(ep))
                continue
        os.makedirs(dir)
        path = os.path.join(dir, "raw.zip")
        with requests.get(url, stream=True, headers=headers) as r:
            with open(path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        with zipfile.ZipFile(path) as f:
            f.extractall(dir)
        for filename in os.listdir(dir):
            if filename.startswith("FIXRepository"):
                filename = os.path.join(dir, filename)
                with zipfile.ZipFile(filename) as f:
                    f.extractall(dir)
        print("-- Successfully downloaded EP{}.xml".format(ep))
        # We wouldn't want to DDOS https://fixtrading.org :)
        time.sleep(6)


if __name__ == "__main__":
    main()
