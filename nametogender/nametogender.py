#!/usr/bin/env python
# encoding: utf-8
from helper import load


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
