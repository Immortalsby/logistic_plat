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
 
    SQLALCHEMY_BINDS = {
        #  'oadb': "mssql+pyodbc:///?odbc_connect=%s" % params 
        'oadb': '{}://{}:{}@{}/{}?driver={}'.format(
            config( 'OADB_ENGINE'   , default='mssql+pyodbc'    ),
            config( 'OADB_USERNAME' , default='HS002'       ),
            config( 'OADB_PASS'     , default='Hs@hanshow#002'          ),
            config( 'OADB_HOST'     , default='172.10.0.132'     ),
            config( 'OADB_NAME'     , default='ecology' ),
            config( 'OADB_DRIVER'     , default='SQL+DRIVER' )
    )
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY  = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600


class DebugConfig(Config):
    DEBUG = True

# Load all possible configurations
oadb_dict = {
    'tables_main': 'id, requestname, AdjReqNum, AdjReqDate, ShipAdress, ShipConPer, ShipPhone, KHMC, CustID',
    'except_part': '400000000001,508100000008,401000100002,401000100001,402000100027',
    'tables_part': 'PartNum, PartDesc, SellingQuantity, KHPOH',
    'tables_ware': 'WLMS, CKLS, WLID',
    'db_main': 'dbo.vw_WorkflowReport_Qzcfh_main',
    'db_part': 'dbo.vw_WorkflowReport_Qzcfh_Dt1',
    'db_ware': 'dbo.vw_WorkflowReport_Qzcfh_Dt2'
}

config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}

xml_url = "https://wms.apex-oms.com/default/svc/web-service/"

app_token = '''</paramsJson>
<appToken>7f27b5da0ed81105b98c35151b54637f</appToken>'''
app_key = '''<appKey>05b92060f873c3c7649339c052a637f5</appKey>'''
body_start = '''<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://www.example.org/Ec/">
	<SOAP-ENV:Body>
		<ns1:callService>
			<paramsJson>'''

body_end = '''</ns1:callService>
	</SOAP-ENV:Body>
</SOAP-ENV:Envelope>'''

xml_dict = {
    'body_start': body_start,
    'data': None,
    'app_token': app_token,
    'app_key': app_key,
    'service': None,
    'body_end': body_end
}

xml_data = {
            "platform":"B2B",
            "warehouse_code":"TESTHANSHOW",
            "shipping_method": "",
            "reference_no": "",
            "country_code": "",
            "province": "province",
            "zipcode":"142970",
            "name": "",
            "address1": "",
            "company": "",
            "order_desc": "",
            "items": ""
            }
