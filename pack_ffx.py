#! /usr/bin/env python
"""
Script to convert a Chrome / Opera WebExtension to a Firefox-compatible WebExtension
Will create a compressed zip archive named from manifest keys <name>_<version>.xpi
Steven Eardley | Cottage Labs LLP
steve@cottagelabs.com
"""

import os
import json
import zipfile
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    "--id",
                    default="firefox_extension@cottagelabs.com",
                    help="The id to be added to the manifest")
parser.add_argument("-v",
                    "--min_version",
                    default="45.0.0",
                    help="The version to put as strict_min_version")
args = parser.parse_args()

ffx_manifest_extras = {
    'applications': {
        'gecko': {
            'id': args.id,
            'strict_min_version': args.min_version
        }
    }
}

chrome_manifest = None

with open('manifest.json') as f:
    try:
        chrome_manifest = json.load(f)
        # change version string to firefox
        try:
            chrome_manifest["version_name"] = chrome_manifest["version_name"].replace('chrome', 'firefox')
        except KeyError:
            # no version_name, pass
            pass

        # add firefox keys to manifest
        chrome_manifest.update(ffx_manifest_extras)
    except ValueError:
        exit(1)

if chrome_manifest is None:
    exit(1)

try:
    name = chrome_manifest['version_name']
except KeyError:
    name = "{0}_firefox_{1}".format(chrome_manifest['name'], chrome_manifest['version'])
archive_filename = '../{0}.xpi'.format(name)

with zipfile.ZipFile(file=archive_filename, mode='w') as xpi_zip:

    # write all files apart from the manifest
    for root, dirs, files in os.walk(os.curdir):
        # exclude hidden files and directories
        files = [f for f in files if not f.startswith('.')]
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for fi in files:

            # add all files to archive except the old manifest and this script
            if fi != 'manifest.json' or fi != 'pack_ffx.py':
                xpi_zip.write(os.path.join(root, fi), compress_type=zipfile.ZIP_DEFLATED)

    # write the updated manifest
    xpi_zip.writestr('manifest.json', json.dumps(chrome_manifest), compress_type=zipfile.ZIP_DEFLATED)

    print "Done. New archive at {0} including:\n".format(archive_filename)
    xpi_zip.printdir()

    xpi_zip.close()
