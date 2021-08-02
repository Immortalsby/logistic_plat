# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present Hanshow
"""

from app.oa import blueprint
from flask import render_template, redirect, url_for, request,flash
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from app.oa.models import get_oadetail, prepare_oadetail, send_oadetail, get_part
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
    details = get_part(detail_one['id'])
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

    return render_template('oa-detail.html', oa_number=oa_number, details=details, error=error, detail_one=detail_one, po_number=po_number, c_code=c_code)

    


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
        order_code = 'Order Code: '+ result['order_code']
    return render_template('oa-detail.html', message=message, order_code=order_code, error=error, oa_number=oa_number)