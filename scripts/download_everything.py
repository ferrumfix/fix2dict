import json
import os
import shutil
import time
import zipfile

import click
import requests

from .download_eps import main as download_eps
from .ep_page_to_links import main as ep_page_to_links


@click.command()
@click.argument("dst", nargs=1, type=click.Path(exists=True))
def main(dst):
    """
    Download everything interesting and useful from <https://www.fixtrading.org>.
    """
    r = requests.get(
        "https://www.fixtrading.org/packages/fix-repository-2010/?wpdmdl=36840")
    # with open(path, 'wb') as f:
    #    shutil.copyfileobj(r.raw, f)
    #    with zipfile.ZipFile(path) as f:
    #        f.extractall(dst)
    #    print("-- Successfully downloaded EP{}.xml".format(ep))


if __name__ == "__main__":
    main()
