# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present Hanshow
"""

import os
from decouple import config

class Config(object):

    basedir    = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')

    # This will create a file in <app> FOLDER
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
    config( 'DB_ENGINE'   , default='mysql+pymysql'    ),
    config( 'DB_USERNAME' , default='logis_user'       ),
    config( 'DB_PASS'     , default='H@nshow123'          ),
    config( 'DB_HOST'     , default='localhost'     ),
    config( 'DB_PORT'     , default=3306           ),
    config( 'DB_NAME'     , default='logis_db' )
    )
    # params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=test;DATABASE=ecology;UID=HS002;PWD=Hs@hanshow#002;Trusted_Connection=yes;') 
    SQLALCHEMY_BINDS = {
        #  'oadb': "mssql+pyodbc:///?odbc_connect=%s" % params 
        'oadb': '{}://{}:{}@{}/{}?driver=/opt/microsoft/msodbcsql/lib64/libmsodbcsql-13.1.so.9.2'.format(
            config( 'OADB_ENGINE'   , default='mssql+pyodbc'    ),
            config( 'OADB_USERNAME' , default='HS002'       ),
            config( 'OADB_PASS'     , default='Hs@hanshow#002'          ),
            config( 'OADB_HOST'     , default='172.10.0.132'     ),
            config( 'OADB_NAME'     , default='ecology' )
    )
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY  = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # MySQL database
    # SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
    #     config( 'DB_ENGINE'   , default='mysql+pymysql'    ),
    #     config( 'DB_USERNAME' , default='logis_user'       ),
    #     config( 'DB_PASS'     , default='H@nshow123'          ),
    #     config( 'DB_HOST'     , default='localhost'     ),
    #     config( 'DB_PORT'     , default=3306           ),
    #     config( 'DB_NAME'     , default='logis_db' )
    # )

class DebugConfig(Config):
    DEBUG = True

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}

xml_url = "https://wms.apex-oms.com/default/svc/web-service"

app_token = '''
			</paramsJson>
			<appToken>7f27b5da0ed81105b98c35151b54637f</appToken>
'''
app_key = '''
			<appKey>05b92060f873c3c7649339c052a637f5</appKey>
'''
body_start = '''
<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://www.example.org/Ec/">
	<SOAP-ENV:Body>
		<ns1:callService>
			<paramsJson>
'''
body_end = '''</ns1:callService>
	</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
'''
xml_dict = {
    'body_start': body_start,
    'data': None,
    'app_token': app_token,
    'app_key': app_key,
    'service': None,
    'body_end': body_end
}

