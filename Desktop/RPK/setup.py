from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'optimize': 2}},
    windows = [{'script': "RPK.py","icon_resources": [(1, "RPK.ico")]}],
    zipfile = "shared.lib",
)
