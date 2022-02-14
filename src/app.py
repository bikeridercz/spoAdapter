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

def add_folder(folder):
    context = ClientContext(config['site_abs_path']).with_credentials(UserCredential(config['username'], config['password']))
    target_folder = config['folder_root_abs_path'] + '/' + folder['ticketId']

    try:
        folder = context.web.get_folder_by_server_relative_url(config['folder_root_rel_path'] + '/' + folder['ticketId']).get().execute_query()
        if folder.exists:
            response = {'resultCode': '-1', 'resultDescription': 'Error: folder already exists', 'folderUrl': target_folder}
            return response
    except ClientRequestException:
        pass
    except Exception as e:
            response = {'resultCode': '-99', 'resultDescription': 'Error: ' + str(e), 'folderUrl': target_folder}
            return response
    
    folder = context.web.folders.add(target_folder).execute_query() #+ ' - ' + folder['ticket_name'] + ' - ' + folder['partner_name'])

    response = {'resultCode': '0', 'resultDescription': 'Success: Folder created successfuly', 'folderUrl': target_folder}
    return response

@app.route('/')
def hello():
   return 'Alive !'

@app.route('/page/newFolder', methods=['GET'])
def api_common():
    return render_template('newFolder.html.jinja')

@app.route('/api/folder/add', methods=['POST'])
def api_add_folder():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        folder = request.get_json()
        response = add_folder(folder)
    elif (content_type in ('application/x-www-form-urlencoded', 'multipart/form-data')):
        form = request.form
        folder = {'ticketId': form['ticketId'], 'ticketType': form['ticketType'], 'ticketSubtype': form['ticketSubtype'], 'partnerId': form['partnerId'], 'createdBy': form['createdBy']}
        response = add_folder(folder)
    else:
        return 'Content-Type not supported: ' + content_type
    #return jsonify(add_order(order))
    #return {'body': new_folder, 'message': 'This endpoint creates the new Folder[{}]'.format(new_folder), 'method': request.method}
    return jsonify(response)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True) #PORT will be redirected in docker to 6080
