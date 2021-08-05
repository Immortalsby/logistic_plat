# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present Hanshow
"""

from app.oa import blueprint
from flask import render_template, redirect, url_for, request,flash
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from app.oa.models import get_oadetail, prepare_oadetail, send_log, send_oadetail, get_oadbinfo, Log
from app.oa.utils import get_country


@blueprint.route('/outbound', methods=['GET', 'POST'])
@login_required
def outbound():
    oa_number = request.form.get('oa_number')
    #return render_template('outbound.html', oa_number=oa_number)
    if oa_number == '' or oa_number == None:
        flash(message="Please Enter A Valid OA Number")
    else:
        return redirect('/outbound/'+oa_number)
    return render_template('outbound.html')


@blueprint.route('/outbound/<oa_number>', methods=['GET', 'POST'])
@login_required
def get_detail(oa_number):
    detail_one = get_oadetail(oa_number)[0]
    details = get_oadbinfo(detail_one['id'],'tables_part','db_part')
    parts = get_oadbinfo(detail_one['id'],'tables_ware','db_ware')
    print(parts)
    if parts != []:
        for detail in details:
            rest = detail['SellingQuantity']
            for part in parts:
                if detail['PartNum'] == part['WLID']:
                    part['shipped'] = 'shipped'
                    part['rest_part'] = rest - int(part['CKSL'])
                    part['total_part'] = detail['SellingQuantity']
                    rest = part['rest_part']
            parts[-1]['shipped'] = None
        print(parts)
    else:
        parts = None
    po_number = details[0]['KHPOH']
    error = None
    c_code = get_country(detail_one['FHGJ'])
    if len(details) == 0:
    #     detail_one = get_oadetail(oa_number)[0]
    # else:
        error = "Not a valid OA Number"
        po_number = None
    print(request.method)
    print(request.form.get('oa_country'))

    return render_template('oa-detail.html', oa_number=oa_number, details=parts, error=error, detail_one=detail_one, po_number=po_number, c_code=c_code)

    


@blueprint.route('/outbound/<oa_number>/send', methods=['GET', 'POST'])
@login_required
def send(oa_number):
    message = None
    error = None
    order_code = None
    g_send_form = dict()
    if request.method == "POST":
        g_send_form = dict()
        g_send_form['country_code'] = request.form.get('oa_country')
        g_send_form['ship_method'] = request.form.get('oa_shipmethod')
        g_send_form['remarks'] = request.form.get('oa_remark')
    requests = prepare_oadetail(oa_number, g_send_form)
    result = send_oadetail(requests)
    if result['ask']=="Failure":
        # error = result['message']
        error = str(result) + str(requests)
    else:
        message = result['message']
        order_code = result['order_code']
    data = {
        "oa_number":oa_number,
        "type":'outbound',
        "c_code": g_send_form['country_code'],
        "ship_method":g_send_form['ship_method'],
        "remark":g_send_form['remarks'],
        "order_code":order_code
    }
    send_log(data)
    return render_template('oa-detail.html', message=message, order_code=order_code, error=error, oa_number=oa_number)


@blueprint.route('/outbound/history', methods=['GET', 'POST'])
@login_required
def get_log():
    details = Log.query.all()
    i = 0
    done = None
    for i in range(len(details)):
        details[i] = str(details[i]).split('|')
        if i == len(details) - 1:
            done = details[i]
    print(details)
    return render_template('outbound_history.html', details=details, done=done)