# -*- coding: utf-8 -*-
"""
    __init__

    :copyright: (c) 2014 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import Pool

from .carrier import Carrier, CarrierZonePriceList


def register():
    Pool.register(
        Carrier,
        CarrierZonePriceList,
        module='carrier_zone', type_='model'
    )
