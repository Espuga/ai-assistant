import re

class APIExecutor:
  def __init__(self, base_url="http://localhost:5000"):
    self.base_url = base_url
    self.api_schema = [
      {
        "description": "Use this endpoint do create a new user.",
        "endpoint": "/users",
        "method": "POST",
        "data": {
          "name": "string",
          "email": "string",
          "password": "string"
        }
      },
      {
        "description": "Use this endpoint to delete a user.",
        "endpoint": "/users/<userId>",
        "method": "DELETE",
        "data": {
          "userId": "integer"
        }
      },
      {
        "description": "Use this endpoint to get a specific user.",
        "endpoint": "/users/<userId>",
        "method": "GET",
        "data": {
          "userId": "integer"
        }
      },
    ]

  def get_api_schema(self):
    return self.api_schema

  def execute_action(self, action):
    import requests
    url = self.base_url + action["endpoint"]
    method = action["method"].upper()
    data = action.get("data", {})
    
    if re.search(r"<.*>", url):
      for key in list(data.keys()):
        if f"<{key}>" in url:
          url = url.replace(f"<{key}>", data[key])
          data.pop(key)

    if method == "POST":
      response = requests.post(url, json=data)
    elif method == "GET":
      response = requests.get(url, params=data)
    elif method == "DELETE":
      response = requests.delete(url, params=data)
    else:
      return {"error": f"Unsupported method: {method}"}

    if response.status_code in [200, 201, 204]:
      return response.json()
    else:
      return {
        "error": f"Status {response.status_code}",
        "detail": response.text
      }
