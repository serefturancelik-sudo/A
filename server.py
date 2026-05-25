from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import os

app = Flask(__name__)
socketio = SocketIO(app)
UPLOAD_FOLDER = 'C:/Phone_Data_Storage'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transfer', methods=['POST'])
def transfer():
    file = request.files['data']
    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)
    
    # Dosya geldiğinde tüm bağlı cihazlara "Dosya Geldi" uyarısı gönder
    socketio.emit('file_received', {'filename': file.filename})
    
    return jsonify({"status": "Dosya Bilgisayara Kaydedildi"})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080)
