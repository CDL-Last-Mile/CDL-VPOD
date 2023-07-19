from flask import render_template, request, Blueprint, redirect, url_for
from vpod.models import (
    OrderDocuments,
    Orders,
    Documents,
    ClientMaster
)
from vpod import db
from sqlalchemy import Date
from datetime import datetime
from vpod.utils import send_error_email
from vpod.config import config

import os

main = Blueprint('main', __name__)


def get_images(client_id=None, date_range=None):
    images = []
    try:
        dbquery = db.session.query(
            Orders.OrderTrackingID,
            Orders.ClientRefNo,
            Orders.PODname,
            Documents.DocumentBinary,
            Documents.FileFormat,
            Documents.IsVisibleOnline,
            OrderDocuments.OrderTrackingID )
        dbquery = dbquery.join(OrderDocuments, Orders.OrderTrackingID == OrderDocuments.OrderTrackingID)
        dbquery = dbquery.join(Documents, OrderDocuments.DocumentID == Documents.DocumentID)

        if client_id is not None: 
            dbquery = dbquery.filter(Orders.ClientID == int(client_id))
            dbquery = dbquery.filter(Documents.IsVisibleOnline == 1)

            #if date range is specified
            if date_range != '' and date_range is not None: 
                threshold = datetime.strptime(date_range, '%Y-%m-%d')
                threshold = threshold.date()

                dbquery = dbquery.filter(Orders.PODcompletion.cast(Date) >= threshold)
            else: 
                #hourly run
                dir_path = os.path.dirname(os.path.realpath(__file__))
                file_path = os.path.join(dir_path, "lastaudit.txt")
                if os.path.exists(file_path) and os.stat(file_path).st_size > 0:
                    with open(file_path, 'r') as f:
                        last_line = f.readlines()[-1]
                        last_line = last_line.strip('\n')
                        if len(last_line) > 0:
                            last_audit = datetime.strptime(last_line.strip('\n'), "%Y-%m-%d %H:%M:%S.%f")
                            dbquery = dbquery.filter(Orders.PODcompletion >= last_audit)
            res = [r._asdict() for r in dbquery.all()]
            client_name = get_client_name(client_id) 
            if client_name:
                # Clean up client name and remove spaces
                client_name = client_name.strip()
                client_name = client_name.replace(" ", "_")
                # Create parent directory
                client_path = "D:\VPOD_IMAGES\\" + client_name
                if date_range != '' and date_range is not None:
                    client_path = client_path + str(date_range)
                # Check if client dir doesn't exist. Create one if it doesn't
                if not os.path.exists(client_path):
                        os.makedirs(client_path)
                for img in res:
                    client_ref_list = []
                    # Check if multiple images with the same clientrefno. clientrefno_1, clientrefno_2
                    if img['ClientRefNo'] in client_ref_list:
                        count = str(client_ref_list.count(img['ClientRefNo']) + 1)
                        file_name = img['ClientRefNo'] +'_' + count + '.' + img['FileFormat']
                    else:
                        file_name = img['ClientRefNo'] + '.' + img['FileFormat']
                    client_ref_list.append(img['ClientRefNo'])
                    image_path = client_path + "\\" + file_name
                    with open(image_path, 'wb') as new_jpg:
                        new_jpg.write(img['DocumentBinary'])
            else: 
                send_error_email(error_msg=e)
                return render_template('error.html')
            return render_template('success.html')
        else: 
            send_error_email(error_msg=e)
            return render_template('error.html')
    except Exception as e: 
        print(e)
        msg = e 
        send_error_email(error_msg=e)
        return render_template('error.html')

def get_hourly_images():
    client_list = config.CLIENT_LIST
    if len(client_list) != 0: 
        for client in client_list: 
            get_images(client_id=client)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "lastaudit.txt")
    append_write = 'w' 
    if os.path.exists(file_path):
        append_write = 'a' # append if already exists
        
    with open(file_path, append_write) as f:
        f.write(str(datetime.now()))
        f.write('\n')
    return True

def get_client_name(client_id=None):
    client_name = ''
    try:
        dbquery = db.session.query(ClientMaster.CompanyName, ClientMaster.ClientID)
        if str(client_id).isdigit():
            dbquery = dbquery.filter(ClientMaster.ClientID == int(client_id))
            dbquery = dbquery.first()
            client_name = dbquery[0]
            return client_name
        else:
            dbquery = dbquery.filter(ClientMaster.CompanyName == client_id)
            dbquery = dbquery.first()
            client_name = dbquery[1]
            return client_name
    except Exception as e: 
        print(e)
        send_error_email(error_msg=e)
        return render_template('error.html')

def get_clients(): 
    clients = []
    
    try: 
        dbquery = db.session.query(ClientMaster.CompanyName)
        res = [r._asdict() for r in dbquery.all()]
        clients = [d['CompanyName'] for d in res]
        return clients
    except Exception as e: 
        print(e)
        send_error_email(error_msg=e)
        return render_template('error.html')

@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')


@main.route("/generate", methods=["POST"])
def generate_rte():
    client_id = request.form.get("client_id")
    date_range = request.form.get("date_range")
    if str(client_id).isdigit():
        client_id = int(client_id)
    else:
        client_id = get_client_name(client_id)
    return get_images(client_id=int(client_id), date_range=date_range)

@main.route("/clients", methods=["GET", "POST"])
def get_clients_rte():
    clients = get_clients()
    return {'data': clients}
    
@main.route("/hourly", methods=["GET", "POST"])
def get_hourly_rte():
    clients = get_hourly_images()
    return {'data': 'Done'}