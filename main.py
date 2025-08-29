from flask import Flask, request, jsonify
import re

app = Flask(__name__)

FULL_NAME = "guruvishwanath_s"
DOB = "17091999"
EMAIL = "your_email@example.com"
ROLL_NUMBER = "22f3000702"

_number_re = re.compile(r"^-?\d+$")

def alternating_caps_reverse(alphabets):
    joined = "".join(alphabets)
    rev = joined[::-1]
    out_chars = []
    for i, ch in enumerate(rev):
        out_chars.append(ch.upper() if i % 2 == 0 else ch.lower())
    return "".join(out_chars)

@app.route("/bfhl", methods=["POST"])
def bfhl():
    try:
        payload = request.get_json(force=True)
        if not isinstance(payload, dict) or "data" not in payload:
            return jsonify({"is_success": False, "message": "JSON must contain 'data' list."}), 400

        data = payload.get("data") or []
        if not isinstance(data, list):
            return jsonify({"is_success": False, "message": "'data' must be a list."}), 400

        numbers = []
        alphabets = []
        specials = []

        for item in data:
            s = str(item)
            if _number_re.match(s):
                numbers.append(s)
            elif s.isalpha():
                alphabets.append(s.upper())
            else:
                specials.append(s)

        odd_numbers = [n for n in numbers if int(n) % 2 != 0]
        even_numbers = [n for n in numbers if int(n) % 2 == 0]
        total_sum = str(sum(int(n) for n in numbers)) if numbers else "0"
        concat_string = alternating_caps_reverse(alphabets)

        resp = {
            "is_success": True,
            "user_id": f"{FULL_NAME}_{DOB}",
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": specials,
            "sum": total_sum,
            "concat_string": concat_string
        }
        return jsonify(resp), 200

    except Exception as e:
        return jsonify({"is_success": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
