import requests

class APIExecutor:
  def __init__(self, base_url="http://localhost:5000"):
    self.base_url = base_url

  def execute_action(self, action):
    """
    Expects 'action' to be a dict like:
    {
      "endpoint": "/users",
      "method": "POST",
      "data": {
        "name": "Ana",
        "email": "ana@example.com"
      }
    }
    """
    url = self.base_url + action['endpoint']
    method = action['method'].upper()
    data = action.get('data', {})

    if method == 'POST':
      response = requests.post(url, json=data)
    elif method == 'GET':
      response = requests.get(url, params=data)
    else:
      return f"Unsupported method: {method}"

    if response.status_code in [200, 201]:
      return f"✅ API call successful: {response.json()}"
    else:
      return f"❌ API call failed: {response.status_code} - {response.text}"
