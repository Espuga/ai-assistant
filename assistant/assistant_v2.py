import ollama
import json
from assistant.api_executor_v2 import APIExecutor_v2

class Assistant_v2():
  def __init__(self, model="mistral"):
    self.model = model
    self.executor = APIExecutor_v2()
    self.api_schema = self.executor.get_api_schema()
    self.tools = self._build_tools_from_schema(self.api_schema)

    self.pending_tool_call = None
    self.pending_missing_field = None

    self.messages = [
      {
        "role": "system",
        "content": """You are a technical assistant that interacts with APIs through function calls (tools). 
If the user's message matches any of the available tools (API endpoints), you MUST call the corresponding tool. 
Do not write example code or assumptions — if required fields are missing, ask the user for them."""
      }
    ]

  def _build_tools_from_schema(self, schema):
    tools = []
    for api in schema:
      tools.append({
        "type": "function",
        "function": {
          "name": self._endpoint_to_tool_name(api["endpoint"], api["method"]),
          "description": f"Call the {api['method']} {api['endpoint']} endpoint.",
          "parameters": {
            "type": "object",
            "properties": {
              k: {"type": "string"} for k in api["data"].keys()
            },
            "required": list(api["data"].keys())
          }
        }
      })
    return tools

  def _endpoint_to_tool_name(self, endpoint, method):
    return f"{method.lower()}_{endpoint.strip('/').replace('/', '_')}"

  def _tool_name_to_api(self, name):
    parts = name.split('_')
    method = parts[0].upper()
    endpoint = '/' + '/'.join(parts[1:])
    return method, endpoint

  def _get_required_fields(self, endpoint, method):
    for api in self.api_schema:
      if api["endpoint"] == endpoint and api["method"] == method:
        return list(api["data"].keys())
    return []

  def send_prompt(self, prompt):
    # If waiting for a missing field
    if self.pending_tool_call and self.pending_missing_field:
      self.pending_tool_call["data"][self.pending_missing_field] = prompt
      required = self._get_required_fields(
        self.pending_tool_call["endpoint"], self.pending_tool_call["method"]
      )
      remaining = [f for f in required if not self.pending_tool_call["data"].get(f)]

      if remaining:
        self.pending_missing_field = remaining[0]
        return f"Please provide the {self.pending_missing_field}"
      else:
        result = self.executor.execute_action(self.pending_tool_call)
        self.pending_tool_call = None
        self.pending_missing_field = None
        return json.dumps(result)

    self.messages.append({"role": "user", "content": prompt})

    response = ollama.chat(
      model=self.model,
      messages=self.messages,
      tools=self.tools
    )

    message = response["message"]
    self.messages.append(message)

    if "tool_calls" in message:
      tool_call = message["tool_calls"][0]
      function_name = tool_call["function"]["name"]
      arguments = tool_call["function"]["arguments"]

      if isinstance(arguments, str):
        arguments = json.loads(arguments)

      method, endpoint = self._tool_name_to_api(function_name)

      required_fields = self._get_required_fields(endpoint, method)
      missing = [f for f in required_fields if not arguments.get(f)]

      if missing:
        # Save state and ask user
        self.pending_tool_call = {
          "endpoint": endpoint,
          "method": method,
          "data": arguments
        }
        self.pending_missing_field = missing[0]
        return f"Please provide the {self.pending_missing_field}"

      result = self.executor.execute_action({
        "endpoint": endpoint,
        "method": method,
        "data": arguments
      })

      self.messages.append({
        "role": "tool",
        "content": json.dumps(result)
      })

      followup = ollama.chat(
        model=self.model,
        messages=self.messages
      )

      self.messages.append(followup["message"])
      return followup["message"]["content"]

    return message["content"]
