# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present Hanshow
"""

from app.oa import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from app.oa.models import get_oadetail, prepare_oadetail, send_oadetail

send_form = {
    'country_code': '',
    'ship_method': '',
    'remarks':''
}

@blueprint.route('/outbound', methods=['GET', 'POST'])
@login_required
def outbound():
    oa_number = request.form.get('oa_number')
    #return render_template('outbound.html', oa_number=oa_number)
    if oa_number == '' or oa_number == None:
        return render_template('outbound.html', message='Please Enter a OA number')
    else:
        return redirect('/outbound/'+oa_number)


@blueprint.route('/outbound/<oa_number>', methods=['GET', 'POST'])
@login_required
def get_detail(oa_number):
    details = get_oadetail(oa_number)
    if len(details):
        send_form['country_code'] = request.form.get('oa_country')
        send_form['ship_method'] = request.form.get('oa_shipmethod')
        send_form['remarks'] = request.form.get('oa_remark')
        detail_one = details[0]
        return render_template('oa-detail.html', oa_number=oa_number, details=details, detail_one=detail_one)
    else:
        error = "Not a valid OA Number"
        return render_template('oa-detail.html', oa_number=oa_number, details=details, error=error)
    


@blueprint.route('/outbound/<oa_number>/send', methods=['GET', 'POST'])
@login_required
def send(oa_number):
    request = prepare_oadetail(oa_number, send_form)
    message = send_oadetail(request)
    print(request)
    return render_template('oa-detail.html', message=message, oa_number=oa_number)