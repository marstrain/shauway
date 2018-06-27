#!venv/bin/python
# coding:utf8

import sys
reload(sys)
sys.setdefaultencoding( "utf8" )
import warnings
warnings.filterwarnings("ignore")
from app  import create_app, db
from app.models import User, Role
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = create_app('development')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)



if __name__ == '__main__':
    manager.run()
