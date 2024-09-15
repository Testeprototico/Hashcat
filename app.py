from flask import Flask, send_file, jsonify, render_template_string
import subprocess
import os
from datetime import datetime

app = Flask(__name__)

LOG_FILE = '/hashcat/logs/hashcat.log'
HASHCAT_CMD = 'hashcat -m 1000 -O -a3 -i hash.txt --outfile /hashcat/logs/hashcat.log'

@app.route('/')
def home():
    return '''
    <html>
    <head>
        <title>Hashcat Service</title>
        <style>
            body { font-family: Arial, sans-serif; }
            .button { padding: 10px 20px; margin: 10px; text-decoration: none; color: white; background-color: #007BFF; border-radius: 5px; }
            .button:hover { background-color: #0056b3; }
        </style>
    </head>
    <body>
        <h1>Welcome to the Hashcat Service</h1>
        <p>Use the following buttons to interact with the service:</p>
        <a href="/start-hashcat" class="button">Start Hashcat</a>
        <a href="/log" class="button">View Log</a>
    </body>
    </html>
    '''

@app.route('/start-hashcat', methods=['GET', 'POST'])
def start_hashcat():
    # Inicie o Hashcat em um processo separado
    subprocess.Popen(HASHCAT_CMD, shell=True)
    return jsonify(message='Hashcat started'), 200

@app.route('/log', methods=['GET'])
def view_log():
    # Verifique se o arquivo de log existe
    if os.path.exists(LOG_FILE):
        # Obter a data e hora da última modificação do log
        last_modified_time = datetime.fromtimestamp(os.path.getmtime(LOG_FILE)).strftime('%Y-%m-%d %H:%M:%S')
        
        # Leia o conteúdo do arquivo de log
        with open(LOG_FILE, 'r') as file:
            log_content = file.read()
        
        # Crie uma página HTML simples para exibir o conteúdo do log e a última atualização
        html_content = f'''
        <html>
        <head>
            <title>Hashcat Log</title>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                pre {{ background: #f0f0f0; padding: 10px; }}
                .button {{ padding: 10px 20px; margin: 10px; text-decoration: none; color: white; background-color: #007BFF; border-radius: 5px; }}
                .button:hover {{ background-color: #0056b3; }}
            </style>
        </head>
        <body>
            <h1>Hashcat Log</h1>
            <p><strong>Last Updated:</strong> {last_modified_time}</p>
            <pre>{log_content}</pre>
            <a href="/" class="button">Back to Home</a>
        </body>
        </html>
        '''
        return render_template_string(html_content)
    else:
        return jsonify(message='Log file not found'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
