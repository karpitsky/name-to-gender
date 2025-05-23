# encoding: utf-8
from __future__ import absolute_import
import os
import csv
import pickle
import zipfile
from io import BytesIO, TextIOWrapper

from six.moves import urllib


NAMES_URL = 'http://www.ssa.gov/oact/babynames/names.zip'


def load(path=None):
    if path:
        datafile = os.path.join(path, 'names.pickle')
    else:
        # First try to load from package directory (for installed package)
        package_dir = os.path.dirname(__file__)
        datafile = os.path.join(package_dir, 'names.pickle')
        
        # If not found in package, try current directory (for development)
        if not os.path.exists(datafile):
            datafile = 'names.pickle'
    
    if os.path.exists(datafile):
        return pickle.load(open(datafile, 'rb'))

    _temp_file = BytesIO()
    _temp_file.write(urllib.request.urlopen(NAMES_URL).read())

    _zip_file = zipfile.ZipFile(_temp_file, 'r')
    names = dict()

    for filename in _zip_file.namelist():
        if '.txt' not in filename:
            continue

        _file = _zip_file.open(filename)
        _file = TextIOWrapper(_file)
        rows = csv.reader(_file, delimiter=',')

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

    for key, value in names.items():
        count = value['M'] + value['F']
        if value['M'] > value['F']:
            value['probability'] = float(value['M']) / count
            value['gender'] = 'M'
        else:
            value['probability'] = float(value['F']) / count
            value['gender'] = 'F'

    # Save to a writable location if we had to download the data
    if not path:
        # Use current directory for development, or user home for installed package
        if os.path.dirname(__file__) in datafile:
            # We're trying to write to package dir, use current dir instead
            save_path = 'names.pickle'
        else:
            save_path = datafile
    else:
        save_path = datafile
    
    _datafile = open(save_path, 'wb')
    pickle.dump(names, _datafile, -1)
    _datafile.close()
    return names


class NameToGender:
    def __init__(self, path=None):
        self.names = load(path=path)

    def name_to_gender(self, name):
        name = name.lower()
        if name not in self.names:
            return dict(name=name, gender=None)

        return dict(
            name=name,
            gender=self.names[name]['gender'],
            probability=self.names[name]['probability']
        )
