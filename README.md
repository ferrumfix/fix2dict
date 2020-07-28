# FIX2dict

![PyPI - Version](https://img.shields.io/pypi/v/fix2dict)
![PyPI - License](https://img.shields.io/pypi/l/fix2dict)

FIX2dict is a FIX Dictionary generator tool.

The program performs data enhancing and data sanitazion on raw FIX Repository files. It allows you to  The resulting data will feature:

- High-quality Markdown documentation obtained from several sources, plus
  minor improvements, e.g.
  * links to ISO standards,
  * RFC 2119 terms capitalization,
  * links for internal navigation,
  * markup, bold text, etc.
- Embedded documentation strings (instead of separate files, like the
  original FIX Repository).
- Full breakdown into fields and components.
- Information about included Extension Packs.
- General cleanup and improved data consistency across all FIX protocol
  versions.

Developers working with the FIX Protocol can really benefit from higher-quality JSON (rather than clunky XML) sources to use for code generation, data explorations, and so on.

In short, FIX2dict makes it much easier to work with the FIX protocol.

## How to use

First, you must install FIX2dict:

    $ pip3 install fix2dict

You can now type `fix2dict --help` for thorough usage information. Here's an example:

    $ fix2dict --improve-docs=1 fix_repository/Unified/ empty/
    Written to 'empty/fix-4-0.json'.
    Written to 'empty/fix-4-1.json'.
    Written to 'empty/fix-4-2.json'.
    Written to 'empty/fix-4-3.json'.
    Written to 'empty/fix-4-4.json'.
    Written to 'empty/fix-5-0.json'.
    Written to 'empty/fix-5-0-sp1.json'.
    Written to 'empty/fixt-1-1.json'.
    Written to 'empty/fix-5-0-sp2.json'.

You can also install from source:

    $ git clone git@github.com:fixipe/fix2dict.git
    $ pip3 install -e fix2dict

## Codebase tour

Main application code is inside `fix2dict/`. `empty/` was introduced as a handy, catch-all target directory for test runs.

`resources/errata` contains random Fix Repository errata in JSON format. It is *not* complete. You should always prefer updating this repository rather than making manual fixes to output files.
`tools/` contains web crawlers for [FixTrading.org](https://fixtrading.org). This allows for automatical download of EP definition files and other useful resources.

## License

Copyright (c) 2020, Filippo Costa. This software is released under the terms of [Apache License 2](https://www.apache.org/licenses/LICENSE-2.0.txt).