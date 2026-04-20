
from flask import Flask, request, render_template_string
from werkzeug.utils import secure_filename
import os

from marymount.edu.receiptscanner.processor import ReceiptScanner

app = Flask(__name__)

scanner = ReceiptScanner()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML = """
<h2>Secure Receipt Scanner</h2>

<form method="POST" enctype="multipart/form-data">
  <input type="file" name="file">
  <input type="submit">
</form>

{% if result %}
<h3>Encrypted Output:</h3>
<p style="word-break: break-all;">{{ result }}</p>
{% endif %}

{% if error %}
<h3 style="color:red;">Error:</h3>
<p>{{ error }}</p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None

    try:
        if request.method == "POST":
            file = request.files["file"]

            if file.filename == "":
                return render_template_string(HTML, error="No file selected")

            filename = secure_filename(file.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)

            file.save(path)

            result = scanner.parse_image(path)

        return render_template_string(HTML, result=result, error=error)

    except Exception as e:
        return render_template_string(HTML, error=str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
