import logging

from odoo.upgrade import util

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info(
        "Removing old modules that are no longer needed:\n - auto_backup\n - interest_on_overdue_invoices\n - theme_georgies"
    )
    util.remove_module(cr, "auto_backup")
    util.remove_module(cr, "interest_on_overdue_invoices")
    util.remove_theme(cr, "theme_georgies")
