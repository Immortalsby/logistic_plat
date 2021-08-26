# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present Hanshow
"""

from flask.globals import request
from flask.helpers import send_from_directory
from sqlalchemy import Binary, Column, Integer, String
from app import db
from flask_login import current_user
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import table
from sqlalchemy.sql.sqltypes import DateTime
from config import config_dict, xml_dict, xml_url, oadb_dict,xml_data
import requests, time
import json
from lxml import etree,html
from app.oa.utils import get_country

class Log(db.Model):

    __tablename__ = 'Log'

    id = Column(Integer, primary_key=True)
    oa_number = Column(String(255))
    type = Column(String(255))
    c_code = Column(String(255))
    ship_method = Column(String(255))
    remark = Column(String(255))
    order_code = Column(String(255))
    create_user = Column(String(255))
    create_date = Column(DateTime)
    result = Column(String(255))

    def __repr__(self):
        return str(self.oa_number)+'|'+str(self.c_code) + '|' + str(self.ship_method) + '|' + str(self.remark) + '|' + str(self.order_code) + '|' +str(self.create_user)+ '|' +str(self.create_date) + '|' + str(self.result)



def get_oadetail(oa_detail):
    app_config = config_dict['Debug']
    engine = create_engine(app_config.SQLALCHEMY_BINDS['oadb'])
    connection = engine.connect()
    tables = oadb_dict['tables_main']
    results = connection.execute("Select {} from {} where AdjReqNum='{}';".format(tables, oadb_dict['db_main'], oa_detail)).fetchall()
    results = [dict(zip(result.keys(), result)) for result in results]
    connection.close()
    return results

def get_oadbinfo(id,table,db):
    app_config = config_dict['Debug']
    engine = create_engine(app_config.SQLALCHEMY_BINDS['oadb'])
    connection = engine.connect()
    tables = oadb_dict[table]
    except_part = 'PartNum' if table == 'tables_part' else 'WLID'
    results = connection.execute("Select {} from {} where mainid={} and {} NOT IN ({});".format(tables, oadb_dict[db], id, except_part,oadb_dict['except_part'])).fetchall()
    results = [dict(zip(result.keys(), result)) for result in results]
    connection.close()
    return results


def prepare_data(main, g_send_form):
    print("id",main[0]['id'])
    # results = get_oadbinfo(main[0]['id'], )
    details = get_oadbinfo(main[0]['id'],'tables_part','db_part')
    parts = get_oadbinfo(main[0]['id'],'tables_ware','db_ware')
    skus, quantitys = [], []
    for detail in details:
        rest = detail['SellingQuantity']
        for part in parts:
            if detail['PartNum'] == part['WLID']:
                part['shipped'] = 'shipped'
                part['rest_part'] = rest - int(part['CKSL'])
                part['total_part'] = detail['SellingQuantity']
                rest = part['rest_part']
        parts[-1]['shipped'] = None
        # skus.append(product['PartDesc'].replace(' ', '').split("；")[0])
        skus.append(parts[-1]['WLID'])
        quantitys.append(parts[-1]['CKSL'])
    items = [{"product_sku": sku,
            #   "product_name_en": "Electronic shelf Label",
              "quantity": quantity} for sku, quantity in zip(skus, quantitys)]
    xml_data['reference_no'] = main[0]['AdjReqNum'] + '_' + main[0]['CustID']
    xml_data['country_code'] = get_country(main[0]['FHGJ'])
    xml_data['name'] = main[0]['ShipConPer']
    xml_data['address1'] = main[0]['XXDZ']
    xml_data['province'] = main[0]['FHCity']
    xml_data['zipcode'] = main[0]['FHYB']
    xml_data['items'] = items
    xml_data['company'] = main[0]['KHMC']
    xml_data['shipping_method'] = g_send_form['ship_method']
    po_number = 'Not recorded' if details[0]['KHPOH'] == None else details[0]['KHPOH']
    xml_data['order_desc'] = "----------PO Number: " + po_number + '----------\n' + g_send_form['remarks']

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
    # print(request)
    # print(request.encode("utf-8"))
    r = requests.post(xml_url, data=request.replace('&amp;', '＆').encode("utf-8"))
    # print(r.content)
    tree = etree.XML(r.content)
    navareas = tree.xpath('//SOAP-ENV:Envelope/SOAP-ENV:Body/ns1:callServiceResponse/response/text()',namespaces={'SOAP-ENV': 'http://schemas.xmlsoap.org/soap/envelope/','ns1': 'http://www.example.org/Ec/'})
    output = ''
    for i in navareas[0]:
	    output += str(i)
    res_list = json.loads(output)
    return res_list


def send_log(data):
    data['create_user'] = current_user.username
    data['create_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    data['result'] = 'fail' if data['order_code'] == None else 'success'
    print(data)
    log = Log(**data)
    db.session.add(log)
    db.session.commit()

def prepare_tracking(oa_number):
    req_dict = xml_dict
    req_dict['service'] = "<service>getOrderByRefCode</service>"
    req_dict['data'] = '''{
        "reference_no": "''' + oa_number + '''"
    }'''
    return prepare_request(req_dict)

def get_tracking_no(oa_number):
    request = prepare_tracking(oa_number)
    r = requests.post(xml_url, data=request.replace('&amp;', '＆').encode("utf-8"))
    print(r.content)
    tree = etree.XML(r.content)
    navareas = tree.xpath('//SOAP-ENV:Envelope/SOAP-ENV:Body/ns1:callServiceResponse/response/text()',namespaces={'SOAP-ENV': 'http://schemas.xmlsoap.org/soap/envelope/','ns1': 'http://www.example.org/Ec/'})
    output = ''
    for i in navareas[0]:
	    output += str(i)
    res_list = json.loads(output)
    return res_list