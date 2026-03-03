import os


DATA_FILE = 'names.csv'
# NAMES_URL = 'https://www.ssa.gov/oact/babynames/names.zip'

_GG_GENDER_MAP = {
    'M': 'M',
    '1M': 'M',
    '?M': 'M',
    'F': 'F',
    '1F': 'F',
    '?F': 'F',
}


def _parse_ssa(path):
    import csv
    import zipfile
    from io import TextIOWrapper

    zf = zipfile.ZipFile(path, 'r')
    counts = {}

    for filename in zf.namelist():
        if '.txt' not in filename:
            continue
        with zf.open(filename) as raw:
            for row in csv.reader(TextIOWrapper(raw), delimiter=','):
                if len(row) < 3:
                    continue
                name = row[0].lower()
                gender = row[1]
                count = int(row[2])
                if name not in counts:
                    counts[name] = [0, 0]
                if gender == 'M':
                    counts[name][0] += count
                else:
                    counts[name][1] += count

    for name, (m, f) in counts.items():
        counts[name] = 'M' if m > f else 'F'

    return counts


def _parse_gender_guesser(path):
    names = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line[0] in '#=':
                continue
            parts = line.split()
            gender = _GG_GENDER_MAP.get(parts[0])
            if not gender:
                continue
            name = parts[1].lower()
            if '+' in name:
                variants = [name.replace('+', r) for r in ['', ' ', '-']]
            else:
                variants = [name]
            for n in variants:
                if n not in names:
                    names[n] = gender
    return names


_PACKAGE_DIR = os.path.dirname(__file__)


def _build_and_save(datafile):
    package_dir = _PACKAGE_DIR

    # SSA data (primary, has counts)
    ssa_zip = os.path.join(package_dir, 'data', 'names.zip')
    names = _parse_ssa(ssa_zip)

    # Gender-guesser data (international names, fills gaps)
    gg_file = os.path.join(package_dir, 'data', 'nam_dict.txt')
    gg_names = _parse_gender_guesser(gg_file)
    for name, gender in gg_names.items():
        if name not in names:
            names[name] = gender

    with open(datafile, 'w') as f:
        for name, gender in sorted(names.items()):
            f.write(f'{name},{gender}\n')

    return names


def load(path=None):
    if path:
        datafile = os.path.join(path, DATA_FILE)
    else:
        datafile = os.path.join(_PACKAGE_DIR, DATA_FILE)

    try:
        names = {}
        with open(datafile) as f:
            for line in f:
                name, gender = line.rstrip('\n').split(',')
                names[name] = gender
        return names
    except FileNotFoundError:
        pass

    return _build_and_save(datafile)


class NameToGender:
    def __init__(self, path=None):
        self.names = load(path=path)

    def name_to_gender(self, name):
        name = name.lower()
        return {'name': name, 'gender': self.names.get(name)}
