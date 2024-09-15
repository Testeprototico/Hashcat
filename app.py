from flask import Flask, send_file, jsonify
import subprocess
import os

app = Flask(__name__)

LOG_FILE = '/hashcat/logs/hashcat.log'
HASHCAT_CMD = 'hashcat -m 1000 -O -a3 -i hash.txt -o /hashcat/logs/hashcat.log'

@app.route('/start-hashcat', methods=['POST'])
def start_hashcat():
    # Inicie o Hashcat em um processo separado
    subprocess.Popen(HASHCAT_CMD, shell=True)
    return jsonify(message='Hashcat started'), 200

@app.route('/download-log', methods=['GET'])
def download_log():
    # Verifique se o arquivo de log existe
    if os.path.exists(LOG_FILE):
        return send_file(LOG_FILE, as_attachment=True)
    else:
        return jsonify(message='Log file not found'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
