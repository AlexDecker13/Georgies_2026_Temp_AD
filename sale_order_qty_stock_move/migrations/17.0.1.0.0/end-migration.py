import logging

from odoo.upgrade import util

_logger = logging.getLogger(__name__)


def hard_reset_view(env, view_id):
    """
    This function resets a view to its default state.

    Parameters:
    env (Environment): The Odoo environment, used for database operations.
    view_id (int): The ID of the view to be reset.

    Returns:
    None

    This function attempts to reset a view to its default state by creating
    a 'reset.view.arch.wizard' record with the view's ID and the reset mode set to 'hard'.
    If an exception occurs during this process, a warning is logged with the view's ID and the exception.
    """
    try:
        view = env["ir.ui.view"].browse(view_id)
        env["reset.view.arch.wizard"].create(
            {"view_id": view.id, "reset_mode": "hard"}
        ).reset_view_button()
    except Exception as e:
        _logger.warning(f"Unable to hard reset view {view_id} due to {e}")


def migrate(cr, version):
    env = util.env(cr)
    _logger.info(
        "Removing old modules that are no longer needed:\n - auto_backup\n - interest_on_overdue_invoice\n - theme_georgies"
    )
    util.remove_module(cr, "auto_backup")
    util.remove_module(cr, "interest_on_overdue_invoice")
    util.remove_theme(cr, "theme_georgies")
    _logger.info("Old modules removed.")
    _logger.info("Reseting views to defaults...")
    hard_reset_view(env, 1486)
    hard_reset_view(env, 1485)
    hard_reset_view(env, 3598)
    hard_reset_view(env, 4093)
    _logger.info("Views reset to defaults.")
