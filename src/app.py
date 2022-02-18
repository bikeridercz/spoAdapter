from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.http.request_options import RequestOptions
from office365.sharepoint.client_context import ClientContext
from office365.runtime.client_request_exception import ClientRequestException
from flask import Flask, request, Response, jsonify, json, render_template
from flask_cors import CORS
import flask, datetime
from config_test import config

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False #Přepíná mezi UTF-8 a českými znaky
CORS(app, resources={r"/*": {"origins": "*"}})

def get_folder(siteId, folderId):
    context = ClientContext(config['site_abs_path']).with_credentials(UserCredential(config['username'], config['password']))

    try:
        folder = context.web.get_folder_by_server_relative_url(config['folder_root_rel_path'] + '/' + folderId).get().execute_query()

        result = 0
        resultCode = 'Success'
        resultDescription = 'Folder exists'

        fields = folder.list_item_all_fields.execute_query()
        fields.get().execute_query()
        folderDetails = {'folderUrl': folder._build_full_url(folder.serverRelativeUrl), 'ticketType': fields.get_property('TicketType',''), 'ticketSubtype': fields.get_property('TicketSubtype',''), 'partnerId': fields.get_property('Partner',''), 'responsiblePerson': fields.get_property('Responsible','')} 
        return {'result': result, 'resultCode': resultCode, 'resultDescription': resultDescription, 'folderDetails': folderDetails}
        
    except ClientRequestException:
        result = -1
        resultCode = 'Error'
        resultDescription = 'Folder does not exists'

    return {'result': result, 'resultCode': resultCode, 'resultDescription': resultDescription, 'folderDetails': None}

def add_folder(folderAttributes):
    folderUrl = None
    folder = None
    context = ClientContext(config['site_abs_path']).with_credentials(UserCredential(config['username'], config['password']))

    try:
        folder = context.web.get_folder_by_server_relative_url(config['folder_root_rel_path'] + '/' + folderAttributes['ticketId']).get().execute_query()
    except ClientRequestException:
        pass

    if folder and folder.exists:
        result = 1
        resultCode = 'Warning'
        resultDescription = 'Folder already exists'
    else:
        result = 0
        resultCode = 'Success'
        resultDescription = 'Folder created successfuly'
        folder = context.web.folders.add(config['folder_root_abs_path'] + '/' + folderAttributes['ticketId']).execute_query()
        fields = folder.list_item_all_fields.execute_query()
        fields.set_property('TicketType', folderAttributes['ticketType'])
        fields.set_property('TicketSubtype', folderAttributes['ticketSubtype'])
        fields.set_property('Partner', folderAttributes['partnerId']).update()
        fields.set_property('Responsible', folderAttributes['responsiblePerson']).update().execute_query()

    folderUrl = folder._build_full_url(folder.serverRelativeUrl)

    return {'result': result, 'resultCode': resultCode, 'resultDescription': resultDescription, 'folderUrl': folderUrl}

@app.route('/')
def hello():
   return 'Alive !'

@app.route('/page/newFolder', methods=['GET'])
def api_common():
    return render_template('newFolder.html.jinja')

@app.route('/api/folder/<folder_id>', methods=['GET'])
def api_get_order(folder_id):
    return jsonify(get_folder('APD', folder_id))
    #return {'body': get_order(order_id), 'message': 'This endpoint returns details of the Order[orderId:{}]'.format(order_id), 'method': request.method}

@app.route('/api/folder/add', methods=['POST'])
def api_add_folder():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        folder = request.get_json()
        response = add_folder(folder)
    elif (content_type in ('application/x-www-form-urlencoded', 'multipart/form-data')):
        form = request.form
        folderAttributes = {'ticketId': form['ticketId'], 'ticketType': form['ticketType'], 'ticketSubtype': form['ticketSubtype'], 'partnerId': form['partnerId'], 'responsiblePerson': form['responsiblePerson']}
        response = add_folder(folderAttributes)
    else:
        return 'Content-Type not supported: ' + content_type
    #return jsonify(add_order(order))
    #return {'body': new_folder, 'message': 'This endpoint creates the new Folder[{}]'.format(new_folder), 'method': request.method}
    return jsonify(response)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True) #PORT will be redirected in docker to 6080
