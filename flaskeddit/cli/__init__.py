from flask.cli import AppGroup

cli_app_group = AppGroup("cli")

from flaskeddit.cli import commands
