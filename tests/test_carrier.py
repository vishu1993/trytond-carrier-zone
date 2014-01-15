# -*- coding: utf-8 -*-
"""
    test_carrier

    Test carrier logic.

    :copyright: (C) 2014 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import sys
import os
DIR = os.path.abspath(os.path.normpath(os.path.join(
    __file__, '..', '..', '..', '..', '..', 'trytond'
)))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))
import unittest
from decimal import Decimal

import trytond.tests.test_tryton
from trytond.transaction import Transaction
from trytond.tests.test_tryton import POOL, DB_NAME, CONTEXT, USER


class TestCarrier(unittest.TestCase):
    '''
    Test carrier
    '''
    def setUp(self):
        """
        Set up data used in the tests.
        this method is called before each test function execution.
        """
        trytond.tests.test_tryton.install_module('carrier_zone')

    def test0010createzone(self):
        '''
        Create a zone and pricelist for it
        '''
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            Carrier = POOL.get('carrier')
            ProductTemplate = POOL.get('product.template')
            Product = POOL.get('product.product')
            UOM = POOL.get('product.uom')
            CarrierZonePriceList = POOL.get('carrier.zone_price_list')
            Currency = POOL.get('currency.currency')
            Country = POOL.get('country.country')
            Party = POOL.get('party.party')

            party, = Party.create([{
                'name': 'Carrier',
            }])
            usd = Currency(
                name='US Dollar', symbol="$", code="USD"
            )
            usd.save()

            template, = ProductTemplate.create([{
                'name': 'Carrier',
                'default_uom': UOM.search([
                    ('name', '=', 'Unit'),
                ])[0].id,
                'type': 'service',
                'list_price': Decimal(0),
                'cost_price': Decimal(0),
            }])
            product, = Product.create([{
                'template': template.id,
            }])

            carrier, = Carrier.create([{
                'zone_currency': usd,
                'carrier_product': product.id,
                'party': party.id,
            }])

            united_states, = Country.create([{
                'name': 'United States',
                'code': 'US',
            }])
            CarrierZonePriceList.create([{
                'carrier': carrier.id,
                'country': united_states.id,
                'price': Decimal('100'),
            }])


def suite():
    """
    Define suite
    """
    test_suite = trytond.tests.test_tryton.suite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestCarrier)
    )
    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
