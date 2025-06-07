from flask import Flask, request, jsonify
import generate_story

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    entries = data.get("entries", [])

    if not entries:
        return jsonify({"error": "No entries provided"}), 400

    # Use your generate_story logic
    story = generate_story.generate_from_entries(entries)

    return jsonify({"story": story})

# This line is ignored by Vercel but useful for local testing
if __name__ == "__main__":
    app.run(debug=True)
