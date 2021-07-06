# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present Hanshow
"""

from flask.globals import request
from flask.helpers import send_from_directory
from sqlalchemy import Binary, Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import table
from config import config_dict, xml_dict, xml_url, oadb_dict,xml_data
import requests
import json
from lxml import etree,html




def get_oadetail(oa_detail):
    app_config = config_dict['Debug']
    engine = create_engine(app_config.SQLALCHEMY_BINDS['oadb'])
    connection = engine.connect()
    tables = oadb_dict['tables']
    results = connection.execute("Select {} from {} where AdjReqNum='{}';".format(tables, oadb_dict['db_name'], oa_detail)).fetchall()
    results = [dict(zip(result.keys(), result)) for result in results]
    connection.close()
    return results

def prepare_data(results, g_send_form):
    skus, quantitys = [], []
    for product in results:
        skus.append(product['PartDesc'].replace(' ', '').split("；")[0])
        quantitys.append(product['SellingQuantity'])
    items = [{"product_sku": sku,
              "product_name_en": "Electronic shelf Label",
              "quantity": quantity} for sku, quantity in zip(skus, quantitys)]
    xml_data['reference_no'] = results[0]['AdjReqNum'] + '_' + results[0]['CustID']
    xml_data['country_code'] = g_send_form['country_code']
    xml_data['name'] = results[0]['ShipConPer']
    xml_data['address1'] = results[0]['ShipAdress']
    xml_data['items'] = items
    xml_data['company'] = results[0]['KHMC']
    xml_data['order_desc'] = "PO Number: " + po_number = 'Not recorded' if results[0]['KHPOH'] == None else results[0]['KHPOH'] + '\n' + g_send_form['remarks']

    return json.dumps(xml_data,ensure_ascii=False)

def prepare_request(req_dict):
    str = ''.join(req_dict.values())
    return str

def prepare_oadetail(oa_number, g_send_form):
    results = get_oadetail(oa_number)
    request_dict = xml_dict
    data = prepare_data(results, g_send_form)
    request_dict['service'] = '<service>createOrder</service>'
    request_dict['data'] = data
    return prepare_request(request_dict)
    
def send_oadetail(request):
    r = requests.post(xml_url, data=request.encode("utf-8"))
    tree = etree.XML(r.content)
    navareas = tree.xpath('//SOAP-ENV:Envelope/SOAP-ENV:Body/ns1:callServiceResponse/response/text()',namespaces={'SOAP-ENV': 'http://schemas.xmlsoap.org/soap/envelope/','ns1': 'http://www.example.org/Ec/'})
    output = ''
    for i in navareas[0]:
	    output += str(i)
    res_list = json.loads(output)
    return res_list
