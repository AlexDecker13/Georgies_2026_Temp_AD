import logging

from odoo.upgrade import util

_logger = logging.getLogger(__name__)

views_to_reset = [1486, 1485, 3598, 4093]
modules_to_remove = ["auto_backup", "interest_on_overdue_invoice", "theme_georgies"]


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
    view = None
    try:
        view = env["ir.ui.view"].browse(view_id)
        env["reset.view.arch.wizard"].create(
            {"view_id": view.id, "reset_mode": "hard"}
        ).reset_view_button()
        return view
    except Exception as e:
        _logger.warning(f"Unable to hard reset view {view_id} due to {e}")
        return view


def migrate(cr, version):
    env = util.env(cr)
    _logger.info(
        "Removing old modules that are no longer needed:\n - auto_backup\n - interest_on_overdue_invoice\n - theme_georgies"
    )
    for module in modules_to_remove:
        util.remove_module(cr, module)

    message = "Uninstalled the following modules:\n"
    message += "\n".join(f"- {module}" for module in modules_to_remove)
    env["ir.logging"].create(
        {
            "name": "UPGRADE: Uninstalled Modules",
            "type": "server",
            "level": "INFO",
            "dbname": cr.dbname,
            "message": message,
            "func": "",
            "path": "",
            "line": "",
        }
    )
    _logger.info("Old modules removed.")

    _logger.info("Reseting views to defaults...")
    reset_views = []
    for view in views_to_reset:
        view = hard_reset_view(env, view)
        if view:
            reset_views.append({"name": view.name, "id": view.id})

    message = "Reset the following views to default:\n"
    message += "\n".join(f"- {view['name']} - {view['id']}" for view in reset_views)
    env["ir.logging"].create(
        {
            "name": "UPGRADE: Reset Views",
            "type": "server",
            "level": "INFO",
            "dbname": cr.dbname,
            "message": message,
            "func": "",
            "path": "",
            "line": "",
        }
    )
    _logger.info("Views reset to defaults.")
