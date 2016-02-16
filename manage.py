from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

from app import create_app, db
from app.models import Passage


def make_shell_context():
    context_dict = {
        "app": app,
        "db": db,
        "Passage": Passage,
    }
    return context_dict


app = create_app("development")

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


if __name__ == "__main__":
    manager.run()
