from flask import Flask, request, jsonify
from search_engine import SemanticSearch
import base64
from PIL import Image
import io
import pytesseract

app = Flask(__name__)
search = SemanticSearch()
search.load_data()

@app.route('/api/', methods=['POST'])
def answer():
    data = request.get_json()
    question = data.get("question", "")

    image_data = data.get("image", None)
    if image_data:
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))
        extracted_text = pytesseract.image_to_string(image)
        question += "\n" + extracted_text.strip()

    results = search.query(question)
    links = [{"url": link, "text": text[:100]} for text, link in results if link]

    return jsonify({
        "answer": results[0][0] if results else "Sorry, I couldn’t find a suitable answer.",
        "links": links
    })

if __name__ == '__main__':
    app.run(debug=True)
