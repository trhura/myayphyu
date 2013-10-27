#! /usr/bin/env python
# Author: Thura Hlaing <trhura@gmail.com>
# Time-stamp: <2013-10-27 18:14:41 (trhura)>

__author__ = "Thura Hlaing <trhura@gmail.com>"

import sys
import os
import csv
import unicodedata

copyright = """
<!--
/*
**
** Copyright 2013, Thura Hlaing <trhura@gmail.com>
**
** DO NOT EDIT
** Autogenerated by keyboard generator script. See scripts/ folder.
*/
-->
"""

opening = """"

<?xml version="1.0" encoding="utf-8"?>
%(copyright)s

""" %locals()

keyboard_open = """
<Keyboard xmlns:android="http://schemas.android.com/apk/res/android"
    android:keyWidth="10%p"
    android:horizontalGap="0px"
    android:verticalGap="0px"
    android:keyHeight="@dimen/key_height">
"""

keyboard_close = """
</Keyboard>
"""

row_open = """
        <Row>
"""

row_close = """
        </Row>
"""

def main():
    for arg in sys.argv[1:]:
        if not os.path.exists (arg):
            print "%(arg)s file doesn't exists." %locals()
            sys.exit(-1)

        content = opening
        with open(arg, mode="r") as csvFile:
            content += keyboard_open

            csvReader = csv.reader(csvFile, delimiter="|", quotechar='"')
            for row in csvReader:
                if not row:
                    continue

                content += row_open

                indent = "\t\t\t"
                for i, key in enumerate(row):
                    key_desc = "<Key "
                    if i == 0:
                        key_desc += 'android:keyEdgeFlags="left" '
                    elif (i + 1) == len(row):
                        key_desc += 'android:keyEdgeFlags="right" '

                    key = key.decode ('utf8').strip().strip('"')

                    attributes = []
                    if key.find(",") == -1:
                        # no csv
                        assert len(key) == 1
                        decimal = ord(key)
                        key_desc += 'android:codes="%(decimal)s" ' %locals()
                        key_desc += 'android:keyIcon="@drawable/sym_%(decimal)s" ' %locals()

                    elif key[0] == u"[":
                        # array
                        assert key.find("]") != -1
                        codes_end=key.find("]")
                        codes = key[1:codes_end]
                        key_desc += 'android:codes="%(codes)s" ' %locals()
                        attributes = key[codes_end+1:].split(",")

                    else:
                        codes_end = key.find(",")
                        codename = key[:codes_end]
                        key_desc += 'android:codes="@integer/key_%(codename)s" ' %locals()
                        attributes = key[codes_end:].split(",")

                    attributes = format_attributes(attributes)
                    key_desc += attributes

                    key_desc += " />"

                    content += indent + key_desc + "\n"
                content += row_close

            content += keyboard_close

        print content

def format_attributes(attributes):
    _attributes = []
    for attr in attributes:
        if not attr:
            continue

        assert attr.find('=') != -1
        key, value = attr.split('=')
        key = key.strip()
        key = "android:" + key

        value = value.strip()
        value = '"%(value)s"' %locals()
        _attributes.append("%(key)s=%(value)s" %locals())

    return " ".join(_attributes)

if __name__ == "__main__":
    main()