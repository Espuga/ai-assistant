from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/users', methods=['POST'])
def create_user():
  data = request.get_json()

  # Required fields
  required_fields = ['name', 'email', 'password']

  # Check for missing fields
  missing_fields = [field for field in required_fields if not data or field not in data or not data[field]]

  if missing_fields:
    return jsonify({
      "error": "Missing required fields",
      "missing": missing_fields
    }), 400

  # Simulate user creation
  user = {
    "name": data["name"],
    "email": data["email"],
    # Do not include the password in a real response!
  }

  print(data)

  return jsonify({
    "message": "User created successfully",
    "user": user
  }), 201

if __name__ == '__main__':
  app.run(debug=False)
