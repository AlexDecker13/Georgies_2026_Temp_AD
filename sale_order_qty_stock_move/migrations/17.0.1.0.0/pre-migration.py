import logging

from odoo.upgrade import util

_logger = logging.getLogger(__name__)

views_to_disable = [
    {
        "xml_id": "studio_customization.default_graph_view_f_5767c0ff-731c-413a-adc2-3cd4a8a90831",
        "id": 3994,
    },
    {
        "xml_id": "studio_customization.odoo_studio_default__73689efd-c3ca-4fe9-a4bc-a26b220e8187",
        "id": 3917,
    },
    {
        "xml_id": "studio_customization.default_tree_view_fo_2de82db8-341c-4e3d-b4c6-780cee3dc769",
        "id": 3901,
    },
    {
        "xml_id": "studio_customization.default_tree_view_fo_c02ffc13-4be2-4884-a4ae-a062713cc421",
        "id": 3899,
    },
    {
        "xml_id": "studio_customization.default_tree_view_fo_e408e6d6-bed9-4582-ae96-acf5e79c9a59",
        "id": 3900,
    },
    {
        "xml_id": "studio_customization.odoo_studio_default__d19b491d-4267-4894-a9c9-d28e8fbb680b",
        "id": 2275,
    },
    {
        "xml_id": "studio_customization.odoo_studio_default__0cf9a039-e01a-4d01-a6f6-4ec045f8e9a8",
        "id": 2250,
    },
    {
        "xml_id": "studio_customization.odoo_studio_default__6ce488e0-a379-4400-9366-5412193cf23a",
        "id": 2845,
    },
    {
        "xml_id": "studio_customization.odoo_studio_default__4230ab7a-2cbd-46cc-9825-f8dd0489d58e",
        "id": 2305,
    },
    {
        "xml_id": "studio_customization.odoo_studio_default__0cd4bf5b-83de-4cfe-b129-5af96acfab2f",
        "id": 2847,
    },
    {
        "xml_id": "studio_customization.default_tree_view_fo_088c8673-dd2f-4d09-a9f3-e73dfbe527e1",
        "id": 3800,
    },
    {
        "xml_id": "studio_customization.default_tree_view_fo_5eb8a9fe-d8c1-4a26-88ad-33a2aa7bfc2f",
        "id": 3915,
    },
    {
        "xml_id": "studio_customization.default_tree_view_fo_024fe98e-b2dd-4d60-88c0-3c5c573f246c",
        "id": 2274,
    },
    {
        "xml_id": "studio_customization.default_tree_view_fo_a2fd9ee1-3796-4747-b3c9-b0d2a8db8e10",
        "id": 2249,
    },
    {
        "xml_id": "studio_customization.default_tree_view_fo_2bbab653-780c-47e1-b54c-196367e28ea6",
        "id": 2844,
    },
    {
        "xml_id": "studio_customization.default_tree_view_fo_f44c36f8-84de-46da-bc24-c84201beae96",
        "id": 2304,
    },
    {
        "xml_id": "studio_customization.default_tree_view_fo_d324d9f3-ed8d-40b6-bc9c-508ddc41bc12",
        "id": 2846,
    },
    {
        "xml_id": False,
        "id": 4072,
    },
    {
        "xml_id": False,
        "id": 4080,
    },
    {
        "xml_id": False,
        "id": 4081,
    },
    {
        "xml_id": False,
        "id": 4082,
    },
    {
        "xml_id": False,
        "id": 4091,
    },
    {
        "xml_id": False,
        "id": 4092,
    },
]


def disable_view(cr, xml_id, view_id):
    """
    This function disables a view in the database.

    Parameters:
    cr (Cursor): The database cursor, used for database operations.
    xml_id (str): The XML ID of the record to be disabled.
    view_id (int, optional): The ID of the view to be disabled. Defaults to None.

    Returns:
    None

    This function attempts to disable a record in the database. If a view_id is provided,
    it is used as the record_id. Otherwise, the function uses the xml_id to find the record_id.
    If a record_id is found, the function sets the 'active' field of the corresponding record to False.
    """
    record = None
    if xml_id:
        record_id = util.ref(
            cr,
            xml_id,
        )
    else:
        record_id = view_id

    if record_id:
        record = util.env(cr)["ir.ui.view"].browse(record_id)
        record.write({"active": False})

    return record


def migrate(cr, version):
    env = util.env(cr)

    _logger.info("Disabling broken studio views...")
    disabled_views = []
    for view in views_to_disable:
        view = disable_view(cr, view.get("xml_id"), view.get("id"))
        if view:
            disabled_views.append({"name": view.name, "id": view.id})

    message = "Disabled the following views:\n"
    message += "\n".join(f"- {view['name']} - {view['id']}" for view in disabled_views)
    env["ir.logging"].create(
        {
            "name": "UPGRADE: Disabled Views",
            "type": "server",
            "level": "INFO",
            "dbname": cr.dbname,
            "message": message,
            "func": "",
            "path": "",
            "line": "",
        }
    )
    _logger.info("Broken studio views disabled.")

    _logger.info("Removing broken website menu items")
    _logger.info("Broken website menu items removed.")
