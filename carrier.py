# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2014 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval, Bool

__all__ = ['Carrier', 'CarrierZonePriceList']
__metaclass__ = PoolMeta


class Carrier:
    __name__ = 'carrier'

    zone_currency = fields.Many2One(
        'currency.currency', 'Currency',
        states={
            'invisible': Eval('carrier_cost_method') != 'zone',
            'required': Eval('carrier_cost_method') == 'zone',
            'readonly': Bool(Eval('zone_price_list', [])),
        },
        depends=['carrier_cost_method', 'zone_price_list'])
    zone_price_list = fields.One2Many(
        'carrier.zone_price_list', 'carrier',
        'Price List',
        states={
            'invisible': Eval('carrier_cost_method') != 'zone',
        },
        depends=['carrier_cost_method'])
    zone_currency_digits = fields.Function(
        fields.Integer(
            'Zone Currency Digits', on_change_with=['zone_currency']
        ), 'on_change_with_zone_currency_digits'
    )

    @classmethod
    def __setup__(cls):
        super(Carrier, cls).__setup__()
        selection = ('zone', 'Zone')
        if selection not in cls.carrier_cost_method.selection:
            cls.carrier_cost_method.selection.append(selection)

    def on_change_with_zone_currency_digits(self, name=None):
        if self.zone_currency:
            return self.zone_currency.digits
        return 2


class CarrierZonePriceList(ModelSQL, ModelView):
    'Carrier Zone price List'
    __name__ = 'carrier.zone_price_list'

    carrier = fields.Many2One('carrier', 'Carrier', required=True, select=True)
    country = fields.Many2One(
        'country.country', 'Country', required=True, select=True
    )
    subdivision = fields.Many2One(
        'country.subdivision', 'Subdivision', select=True,
        domain=[('country', '=', Eval('country'))],
        depends=['country']
    )
    price = fields.Numeric(
        'Price', digits=(16, Eval('_parent_carrier.weight_currency_digits', 2))
    )
