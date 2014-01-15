# -*- coding: utf-8 -*-
"""
    __init__

    :copyright: (c) 2014 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import Pool


def register():
    Pool.register(
        module='carrier_zone', type_='model'
    )
