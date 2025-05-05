from odoo import models, api,fields


class AccountFilterPartnerLedger(models.AbstractModel):
    _inherit = 'account.partner.ledger.report.handler'

    def _get_custom_display_config(self):
        return {
            'templates': {
                'AccountReportFilters': 'account_report_filter_account.AccountFilterAccount',
            },
        }

class AccountGeneralLeadger(models.AbstractModel):
    _inherit = 'account.general.ledger.report.handler'

    def _get_custom_display_config(self):
        return {
            'templates': {
                'AccountReportFilters': 'account_report_filter_account.AccountFilterAccount',
            },
        }

class AccountTrialBalance(models.AbstractModel):
    _inherit = 'account.trial.balance.report.handler'

    def _get_custom_display_config(self):
        return {
            'templates': {
                'AccountReportFilters': 'account_report_filter_account.AccountFilterAccount',
            },
        }

class AccountBalanceSheet(models.AbstractModel):
    _inherit = 'account.balance.sheet.report.handler'

    def _get_custom_display_config(self):
        return {
            'templates': {
                'AccountReportFilters': 'account_report_filter_account.AccountFilterAccount',
            },
        }


class AccountReport(models.Model):
    _inherit = 'account.report'

    def _get_filter_accounts(self, options):
        """
        Function to filter the account's in the filter drop down.
        """
        item = [
            {'id': rec.id, 'display_name': rec.display_name, 'selected': False}
            for rec in
            self.env['account.account'].search([('company_ids', 'in',
                                                 models.to_company_ids(
                                                     self.env.company))])]
        return item

    def _init_options_accounts(self, options, previous_options):
        all_accounts = self._get_filter_accounts(options)
        previous_accounts = previous_options.get('account_id', [])
        options['account_id'] = []
        options['selected_account_ids'] = {}
        groups_account_selected = set()
        previous_selected_account_ids = {
            account['id'] for account in previous_accounts if
            account.get('selected')
        }
        for account in all_accounts:
            if account.get('id') in previous_selected_account_ids:
                account['selected'] = True
            else:
                account['selected'] = False
        if all_accounts:
            options['account_id'] = all_accounts

    @api.model
    def _get_options_account_id_domain(self, options):
        """Domain creating based on the selection."""
        domain = []
        selected_journals = [
            account for account in options.get('account_id', [])
            if account['selected']
        ]
        if selected_journals:
            account_ids = [int(account.get('id')) for account in
                           selected_journals]
            domain.append(('account_id', 'in', account_ids))
        return domain

    def _get_options_domain(self, options, date_scope):
        res = super()._get_options_domain(options, date_scope)

        return res + self._get_options_account_id_domain(options)
