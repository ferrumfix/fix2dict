import click


def opt_ep(arg_name):
    return lambda funct: click.option(
        "--ep",
        arg_name,
        multiple=True,
        help=(
            "Include this Expansion Pack file (.xml) " "into the final Fix Dictionary."
        ),
        type=click.Path(exists=True),
    )(funct)


def opt_patch(arg_name):
    return lambda funct: click.option(
        "--patch",
        "-p",
        arg_name,
        multiple=True,
        help=("Provide a JSON Patch file to apply to final data. " "Follows RFC 6902."),
        type=click.Path(exists=True),
    )(funct)


def opt_typos(arg_name):
    return lambda funct: click.option(
        "--typos",
        arg_name,
        multiple=True,
        help="Provide a JSON typos file.",
        type=click.Path(exists=True),
    )(funct)


def opt_markdownify(arg_name):
    return lambda funct: click.option(
        "--markdownify",
        "-m",
        arg_name,
        default=False,
        is_flag=True,
        help=("Perform data enhancing on documentation strings. " "Off by default."),
    )(funct)


def opt_improve_docs(arg_name):
    return lambda funct: click.option(
        "--improve-docs",
        arg_name,
        default=False,
        is_flag=True,
        help=("Perform data enhancing on documentation strings." "Off by default."),
    )(funct)


def opt_yaml(arg_name):
    return lambda funct: click.option(
        "--yaml",
        arg_name,
        default=False,
        is_flag=True,
        help="Also emit YAML besides JSON. Off by default.",
    )(funct)
