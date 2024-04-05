from flask import Flask, render_template, request, Response, jsonify
import time

app = Flask(__name__)

# 首頁
@app.route('/')
def index():
    return render_template('download.html')

@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            print(f'下載影片： {url}')
            
            return jsonify({'status': 'success', 'url': url})
        else:
            return jsonify({'status': 'error', 'message': 'Missing URL parameter'})
    else:
        return jsonify({'status': 'error', 'message': 'Method Not Allowed'}), 405
    
@app.route('/progress', methods=['GET'])
def progress():
    def generate():
        for i in range(101):
            time.sleep(0.1)
            yield f"data:{i}\n\n"
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
