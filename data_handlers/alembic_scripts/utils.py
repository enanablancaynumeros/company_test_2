from os import path
from glob import glob

from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory
from models.postgres import *


alembic_cfg = Config()
scripts_folder = path.dirname((path.abspath(__file__)))
alembic_cfg.set_main_option("script_location", scripts_folder)
script = ScriptDirectory.from_config(alembic_cfg)


def alembic_upgrade_head():
    command.upgrade(alembic_cfg, revision="head")


def generate_migration_script():
    rev_id = get_next_id()
    command.revision(
        alembic_cfg, autogenerate=True, rev_id=rev_id, message="Change this"
    )


def format_revision(rev_id):
    """
    Args:
        rev_id (Union[int, str]):

    Returns:
        str
    """
    if (
        isinstance(rev_id, int)
        or rev_id not in {"base", "head"}
        and not rev_id.startswith("0")
    ):
        return f"0{rev_id}"
    return rev_id


def get_next_id():
    all_files = get_all_script_files()
    if all_files:
        rev_id = max(int(path.basename(x).split("_")[0]) for x in all_files)
        rev_id += 1
    else:
        rev_id = 0
    rev_id = format_revision(rev_id)
    return rev_id


def get_all_script_files():
    versions_folder = path.join(scripts_folder, "versions/*.py")
    return glob(versions_folder)
