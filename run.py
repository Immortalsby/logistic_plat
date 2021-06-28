# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present Hanshow
"""

from flask_migrate import Migrate
from os import environ
from sys import exit
from decouple import config
import logging

from config import config_dict
from app import create_app, db

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# The configuration 
get_config_mode = 'Debug' if DEBUG else 'Production'
print("----------------------------"+get_config_mode)
try:
    
    # Load the configuration using the default values 
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app( app_config )
Migrate(app, db)



# from sqlalchemy import create_engine

# from sqlalchemy.orm import sessionmaker
# engine = create_engine(app_config.SQLALCHEMY_BINDS['oadb'])

# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base(engine)

# Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
# session = Session()
# print('----Session----:',dir(Session))
# print('----Base----:',dir(Base))


if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG)      )
    app.logger.info('Environment = ' + get_config_mode )
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI )
    app.logger.info('DBSSMS      = ' + app_config.SQLALCHEMY_BINDS['oadb'] )

if __name__ == "__main__":
    app.run(debug=true,port=80)
