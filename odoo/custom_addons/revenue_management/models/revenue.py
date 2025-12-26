from odoo import api, fields, models


class Revenue(models.Model):
    _name = 'revenue.management.revenue'
    _description = 'Revenue'

    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    amount = fields.Float(string='Amount', required=True, default=0.0)
    description = fields.Text(string='Description')

    @api.model
    def total_revenue(self, date_from=None, date_to=None):
        """Return total amount in the given date range (inclusive)."""
        domain = []
        if date_from:
            domain.append(('date', '>=', date_from))
        if date_to:
            domain.append(('date', '<=', date_to))
        records = self.search(domain)
        return sum(records.mapped('amount'))

