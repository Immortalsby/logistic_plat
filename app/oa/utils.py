# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present Hanshow
"""


def get_country(c):
    c = c.lower()
    print(c)
    if c in ('be','belgium','belgique','belgië', 'belgië'):
        c = 'BE'
    elif c in ('france', 'fr'):
        c = 'FR'
    elif c in ('germany', 'deutschland', 'de'):
        c = 'DE'
    elif c in ('netherlands', 'holland', 'nederlanden', 'nl'):
        c = 'NL'
    elif c in ('luxembourg', 'lu'):
        c = 'LU'
    else:
        c = 'Country not available'
    return c
