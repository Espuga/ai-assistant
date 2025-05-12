class APIExecutor_v2:
  def __init__(self, base_url="http://localhost:5000"):
    self.base_url = base_url
    self.api_schema = [
      {
        "endpoint": "/users",
        "method": "POST",
        "data": {
          "name": "string",
          "email": "string",
          "password": "string"
        }
      }
    ]

  def get_api_schema(self):
    # Optionally load from DB instead
    return self.api_schema

  def execute_action(self, action):
    import requests
    url = self.base_url + action["endpoint"]
    method = action["method"].upper()
    data = action.get("data", {})

    if method == "POST":
      response = requests.post(url, json=data)
    elif method == "GET":
      response = requests.get(url, params=data)
    else:
      return {"error": f"Unsupported method: {method}"}

    if response.status_code in [200, 201]:
      return response.json()
    else:
      return {
        "error": f"Status {response.status_code}",
        "detail": response.text
      }
