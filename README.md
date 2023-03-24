# Tile matching tools

![Tests](https://github.com/inf122-tmge-winter-2023/tile-matching-tools/actions/workflows/package-test.yml/badge.svg)

## About

A python package providing a set of extensible tools that simplify the process of building you very own tile-matching game. The package breaks down the components of a tile-matching game into its `model`, `view` and `core` components. A minimal game will only utilize or extend classes from the `core` and `view` submodules. For more features, extend classes in the `model` submodule. For more information on the the submodules and individual classes, view the docs [here](https://inf122-tmge-winter-2023.github.io/tilematch-tools-docs/)

## Getting started

### Installation

It is recommended to install this package (along with any others) in its own virtual environment to best ensure capatiblity amongst all dependencies. Once you've set up a virtual environment, run the following command 

```bash
pip install tilematch_tools@git+https://github.com/inf122-tmge-winter-2023/tile-matching-tools
```

If you have other dependecies, you can add the following line the your `requirements.txt` file in your project

```bash
tilematch_tools@git+https://github.com/inf122-tmge-winter-2023/tile-matching-tools
```

### Caveats

- Python 3.11 or newer is required, so update your freakin Python already
- GUI depends on the `tkinter` module. On unix machines, it may be installed separately from your python install

## Known issues

View them [here](https://github.com/inf122-tmge-winter-2023/tile-matching-tools/issues)

## Contributers

- Nathan Mendoza (nathancm@uci.edu)
- Matthew Isayan
