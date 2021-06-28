# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present Hanshow
"""

from flask.globals import request
from sqlalchemy import Binary, Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import table
from config import config_dict, xml_dict, xml_url
import requests
import json


def get_oadetail(oa_detail):
    app_config = config_dict['Debug']
    engine = create_engine(app_config.SQLALCHEMY_BINDS['oadb'])
    connection = engine.connect()
    tables = "requestname,AdjReqNum,AdjReqDate,ShipAdress,ShipConPer,ShipPhone,KHMC,CustID,PartNum,PartDesc,SellingQuantity"
    results = connection.execute("Select {} from dbo.vw_WorkflowReport_QZCFH where AdjReqNum='{}';".format(tables, oa_detail)).fetchall()
    results = [dict(zip(result.keys(), result)) for result in results]
    connection.close()
    return results

def prepare_data(results):
    skus, quantitys = [], []
    for product in results:
        skus.append(product['PartDesc'].replace(' ', '').split("；")[0])
        quantitys.append(product['SellingQuantity'])
    items = [{"product_sku": sku,
              "product_name_en": "Electronic shelf Label",
              "quantity": quantity} for sku, quantity in zip(skus, quantitys)]
    data = {
            "platform":"OTHER",
            "warehouse_code":"TESTHANSHOW",
            "shipping_method":"UPS_DELIVERY",
            "reference_no": results[0]['AdjReqNum'],
            "country_code":"FR",
            "province":"province",
            "name": results[0]['ShipConPer'],
            "address1":results[0]['ShipAdress'],
            "zipcode":"12970",
            "items": items
            }

    return json.dumps(data,ensure_ascii=False)

def prepare_request(req_dict):
    return req_dict['body_start']+req_dict['data']+req_dict['app_token']+req_dict['app_key']+req_dict['service']+req_dict['body_end']

def prepare_oadetail(oa_number):
    results = get_oadetail(oa_number)
    request_dict = xml_dict
    data = prepare_data(results)
    request_dict['service'] = '<service>createOrder</service>'
    request_dict['data'] = data
    return prepare_request(request_dict)
    
def send_oadetail(request):
    print(type(request))
    print(request)
    str1 = '''<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://www.example.org/Ec/">
        <SOAP-ENV:Body>
                <ns1:callService>
                        <paramsJson>
{"platform": "OTHER", "warehouse_code": "TESTHANSHOW", "shipping_method": "UPS_DELIVERY", "reference_no": "HS-QZCFH-2021-01-10-0061", "country_code": "FR", "province": "province", "name": "Bricoman Le mans", "address1": "Yvre Lieu Dit ＇La Fanière＇72530   YVRE", "zipcode": "12970", "items": [{"product_sku": "Stellar-S3TN@E31A", "product_name_en": "Electronic shelf Label", "quantity": 1500}]}
                        </paramsJson>
                        <appToken>7f27b5da0ed81105b98c35151b54637f</appToken>

                        <appKey>05b92060f873c3c7649339c052a637f5</appKey>
<service>createOrder</service></ns1:callService>
        </SOAP-ENV:Body>
</SOAP-ENV:Envelope>'''.strip()
    str2 = request.strip()

    li1 = []
    li2 = []
    for i in str1:
        if i==" ":
            continue
        li1.append(i)
    print(li1)
    for j in str2:
        if j==" ":
            continue
        li2.append(j)
    print(li2)
    for x in range(len(li1)):
        if li1[x]!=li2[x]:
            print(x,li1[x],li2[x])
    r = requests.post(xml_url, data=request.encode("utf-8"))
    print(r.text, r.ok)
    return r
# class Oa_detail(db.Model):
#     __bind_key__ = 'oadb'
#     __tablename__ = 'dbo.vw_WorkflowReport_QZCFH'
    
#     # id = Column(Integer, primary_key=True)
#     AdjReqNum = db.Column(db.String(99), primary_key=True)
#     ShopName = db.Column(db.String(999))
#     ShipAdress = db.Column(db.String(999))
#     ShipConPer = db.Column(db.String(999))
#     ShipPhone = db.Column(db.String(999))
#     PartNum = db.Column(db.String(1000))
#     PartDesc = db.Column(db.String(299))
#     SellingQuantity = db.Column(Integer)
