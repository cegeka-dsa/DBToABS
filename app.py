from flask import Flask, render_template, request, redirect, url_for
from db_to_abs import export_to_blob

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/export', methods=['POST'])
def export():
    try:
        server = request.form['server']
        database = request.form['database']
        username = request.form['username']
        password = request.form['password']
        separator = request.form['separator']
        escapechar = request.form['escapechar']
        encoding = request.form['encoding']
        tenant_id = request.form['tenant_id']
        client_id = request.form['client_id']
        client_secret = request.form['client_secret']
        storage_account_name = request.form['storage_account_name']
        container_name = request.form['container_name']

        # Call the export function with user inputs
        export_to_blob(server, database, username, password, separator, 
                      escapechar, encoding, tenant_id, client_id, 
                      client_secret, storage_account_name, container_name)

        return render_template('response.html', error=None)
    except Exception as e:
        return render_template('response.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)