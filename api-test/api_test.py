from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/users', methods=['POST'])
def create_user():
  data = request.get_json()

  # Required fields
  required_fields = ['name', 'email', 'password']

  # Check for missing fields
  missing_fields = [field for field in required_fields if not data or field not in data or not data[field]]

  # Is missing fields
  if missing_fields:
    return jsonify({
      "error": "Missing required fields",
      "missing": missing_fields
    }), 400

  user = {
    "name": data["name"],
    "email": data["email"],
  }

  print(data)

  return jsonify({
    "message": "User created successfully",
    "user": user
  }), 201
  
@app.route("/users/<userId>", methods=['DELETE'])
def delete_user(userId):
  print(f"User ID to delete: {userId}")
  return jsonify({
    "message": "User deleted successfully"
  }), 200
  
@app.route("/users/<userId>", methods=['GET'])
def get_user(userId):
  print(f"Get info from user: {userId}")
  user = {
    "name": "Test name",
    "email": "Test email",
  }
  return jsonify({
    "message": "User created successfully",
    "user": user
  }), 201

if __name__ == '__main__':
  app.run(debug=False)
