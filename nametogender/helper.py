#!/usr/bin/env python
# encoding: utf-8
import os
import csv
import pickle
import urllib2
import StringIO
import zipfile

DATAFILE = 'names.pickle'
NAMES_URL = 'http://www.ssa.gov/oact/babynames/names.zip'


def load(path=None):
    if path:
        DATAFILE = path + DATAFILE
    if os.path.exists(DATAFILE):
        return pickle.load(open(DATAFILE, 'rb'))

    _temp_file = StringIO.StringIO()
    _temp_file.write(urllib2.urlopen(NAMES_URL).read())

    _zip_file = zipfile.ZipFile(_temp_file, 'r')
    names = dict()

    for filename in _zip_file.namelist():
        if '.txt' not in filename:
            continue

        _file = _zip_file.open(filename, 'rU', 'utf-16')
        rows = csv.reader(_file.read().splitlines(), delimiter=',')

        for row in rows:
            if len(row) < 3:
                continue
            name = row[0].lower()
            gender = row[1]
            count = int(row[2])

            if name not in names:
                names[name] = dict(M=0, F=0)
            names[name][gender] = names[name][gender] + count

        _file.close()

    for key, value in names.iteritems():
        count = value['M'] + value['F']
        if value['M'] > value['F']:
            value['probability'] = float(value['M']) / count
            value['gender'] = 'M'
        else:
            value['probability'] = float(value['F']) / count
            value['gender'] = 'F'

    _datafile = open(DATAFILE, 'wb')
    pickle.dump(names, _datafile, -1)
    _datafile.close()
    return names
