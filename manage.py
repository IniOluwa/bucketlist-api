
"""
Flask app blueprint manage
This file starts the flask app
"""
# Denpendency importation for manage
from app import create_app, db
from app.models import User, BucketList, BucketListItem
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

# app, manager, migrate execution of flask app
app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)


# App shell context created
def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User,
        BucketList=BucketList,
        BucketListItem=BucketListItem
        )

# Shell context added to manager for command line execution
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


# App test runner
@manager.command
def test():
    """Running the tests by blueprint convention"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

# App run
if __name__ == '__main__':
    manager.run()
