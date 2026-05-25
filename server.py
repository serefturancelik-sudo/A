from flask import Flask, request, jsonify, render_template_string
import time
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'C:/Phone_Data_Storage'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# HTML Arayüzü (Kullanıcı bu sayfayı telefonundan açacak)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<body>
    <h2>Çipil Data Bridge</h2>
    <input type="file" id="fileInput">
    <button onclick="upload()">Veriyi Gönder & Hız Testi Yap</button>
    <div id="result"></div>
    <script>
        async function upload() {
            const file = document.getElementById('fileInput').files[0];
            const formData = new FormData();
            formData.append('data', file);
            const start = performance.now();
            const res = await fetch('/transfer', {method: 'POST', body: formData});
            const data = await res.json();
            const end = performance.now();
            document.getElementById('result').innerText = "Sonuç: " + data.status + " | Hız: " + data.speed + " MB/s";
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/transfer', methods=['POST'])
def transfer():
    start = time.time()
    file = request.files['data']
    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)
    duration = time.time() - start
    size_mb = os.path.getsize(save_path) / (1024 * 1024)
    return jsonify({"status": "Başarılı", "speed": round(size_mb / duration, 2)})

if __name__ == '__main__':
    # Bilgisayarının yerel IP'sini buraya yazmalısın (örn: 192.168.1.5)
    app.run(host='0.0.0.0', port=8080)
