# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.addons.decimal_precision import decimal_precision as dp
from datetime import datetime

class HitrateReport(osv.Model):

    _name = "sale_hitrate_report.report"
    _description = 'Hitrate Report'

    def _form_sale_domain(self, report):
        '''You can override this method to customize the results.'''
        domain = [('company_id', '=', report.company_id.id),
                  ('currency_id', '=', report.currency_id.id),
                  ('date_order', '>=', report.date_start),
                  ('date_order', '<=', report.date_end),
                  ('state', 'in', ['progress', 'manual', 'invoice_except', 'shipping_except', 'done'])]
        return domain

    def _form_non_sale_domain(self, report):
        '''You can override this method to customize the results.'''
        domain = [('company_id', '=', report.company_id.id),
                  ('currency_id', '=', report.currency_id.id),
                  ('date_order', '>=', report.date_start),
                  ('date_order', '<=', report.date_end),
                  ('state', 'not in', ['progress', 'manual', 'invoice_except', 'shipping_except', 'done'])]
        return domain

    def _generate_report(self, cr, uid, ids, name, arg, context=None):

        result = {}

        sale_order_model = self.pool.get('sale.order')
        for report in self.browse(cr, uid, ids, context=context):

            sale_domain = self._form_sale_domain(report)
            sale_ids = sale_order_model.search(cr, uid, args=sale_domain)
            '''Convert to float to prevent integer truncation when dividing later.'''
            sale_count = float(len(sale_ids))

            non_sale_domain = self._form_non_sale_domain(report)
            non_sale_ids = sale_order_model.search(cr, uid, args=non_sale_domain)
            non_sale_count = float(len(non_sale_ids))

            if sale_count > 0 or non_sale_count > 0:
                hitrate = sale_count / (sale_count + non_sale_count) * 100
            else:
                hitrate = 0.00

            sale_totals = 0.00
            non_sale_totals = 0.00

            for so in sale_order_model.browse(cr, uid, sale_ids, context):
                sale_totals += so.amount_total

            for nso in sale_order_model.browse(cr, uid, non_sale_ids, context):
                non_sale_totals += nso.amount_total

            result[report.id] = {
                'name': '{}, {} - {} ({})'.format(report.company_id.name, report.date_start, report.date_end, report.currency_id.name),
                'sale_ids': sale_ids,
                'sale_count': sale_count,
                'sale_totals': sale_totals,
                'non_sale_ids': non_sale_ids,
                'non_sale_count': non_sale_count,
                'non_sale_totals': non_sale_totals,
                'hitrate': hitrate,
            }

        return result

    _columns = {
        'name': fields.function(_generate_report, string="Name", type="char", multi="report_calc"),
        'date_start': fields.date('Start date', required=True),
        'date_end': fields.date('End date', required=True),
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'currency_id': fields.many2one('res.currency', 'Currency', required=True),
        'notes': fields.text('Notes'),

        'sale_count': fields.function(_generate_report, string="Sale count", type="integer", multi="report_calc"),
        'non_sale_count': fields.function(_generate_report, string="Non-sale count", type="integer", multi="report_calc"),
        'sale_totals': fields.function(_generate_report, string="Sale Totals", type="float", multi="report_calc"),
        'non_sale_totals': fields.function(_generate_report, string="Non-sale Totals", type="float", multi="report_calc"),

        'hitrate': fields.function(_generate_report, string="Hit rate (%)", type="float", multi="report_calc"),
        'sale_ids': fields.function(_generate_report,
                                    relation='sale.order',
                                    string="Sales",
                                    type='many2many',
                                    multi='report_calc'),

        'non_sale_ids': fields.function(_generate_report,
                                        relation='sale.order',
                                        string="Non-sales",
                                        type='many2many',
                                        multi='report_calc'),
    }

    _defaults = {
        'company_id': lambda self,cr,uid,context: self.pool.get('res.users').browse(cr,uid,uid,context).company_id.id,
        'currency_id': lambda self,cr,uid,context: self.pool.get('res.users').browse(cr,uid,uid,context).company_id.currency_id.id,
        'date_start': lambda self,cr,uid,context: '{0}-01-01'.format(str(datetime.now().year)),
        'date_end': lambda self,cr,uid,context: '{0}-12-31'.format(str(datetime.now().year)),
    }
