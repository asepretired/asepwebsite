from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import subprocess
import tempfile
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def health():
    return jsonify({"status": "ok", "service": "luraph-deobfuscator-backend"})

@app.route('/api/fetch-url', methods=['POST'])
def fetch_url():
    """Fetch script dari URL raw (mengatasi CORS)."""
    data = request.get_json()
    target_url = data.get('url')
    if not target_url:
        return jsonify({'error': 'URL diperlukan'}), 400
    try:
        resp = requests.get(target_url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; LuraphDeobfuscator/1.0)'
        })
        resp.raise_for_status()
        return Response(resp.text, mimetype='text/plain')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/deobfuscate', methods=['POST'])
def deobfuscate():
    """Jalankan tool deobfuscator (placeholder — sesuaikan dengan tool-mu)."""
    tool = request.form.get('tool', 'luraph-deobfuscator-py')
    raw_text = request.form.get('raw_text', '')
    file = request.files.get('file')

    if not raw_text and not file:
        return jsonify({'error': 'Tidak ada input'}), 400

    # Simpan input ke temp file
    script_content = raw_text if raw_text else file.read().decode('utf-8')
    with tempfile.NamedTemporaryFile(mode='w', suffix='.lua', delete=False) as f:
        f.write(script_content)
        input_path = f.name

    try:
        # TODO: Ganti dengan perintah tool deobfuscator yang sebenarnya
        # Contoh: subprocess.run(['python', 'path/to/deobfuscator.py', input_path], ...)
        result = f"-- Deobfuscated dengan {tool}\n-- (Placeholder — integrasikan tool di sini)\n\n{script_content}"
        return Response(result, mimetype='text/plain')
    finally:
        os.unlink(input_path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
