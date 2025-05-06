import ollama
import json
from assistant.api_executor import APIExecutor

class Assistant():
  def __init__(self, model="mistral"):
    self.model = model
    self.executor = APIExecutor()

    self.pending_action = None
    self.pending_field = None

    # Api Schema
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


    # Initial system message
    init_prompt = f"""
      You are a technical assistant that helps execute API actions.

      Available API endpoints:
      {json.dumps(self.api_schema, indent=2)}

      Instructions:
      - When the user gives a command, match it with the correct API endpoint based on method and intent, in case of the command didn't match with any API endpoint, return:
        {{
          "action": "no_api",
          "message": "There is no API for that action"
        }}
      - Check that all the fields are in the data to send, if any required field is missing, return the following JSON replacing the message value to the question asking by the missing field and also replacing the pending_action.endpoint and pending_action.method by the endpoint that have to be used:
        {{
          "action": "ask_user",
          "message": "question",
          "pending_action": {{
            "action": "call_api",
            "endpoint": "endpoint name",
            "method": "endpoint method",
            "data": {{}}
          }}
        }}
      - If ALL required data fields are present, return:
        {{
          "action": "call_api",
          "endpoint": "/example",
          "method": "POST",
          "data": {{...}}
        }}

      Return ONLY valid JSON. No explanations.
    """
    self.messages = [{'role': 'system', 'content': init_prompt}]


  def send_prompt(self, prompt):

    if self.pending_action and self.pending_field:
      # Fill in the missing field with the user's response
      self.pending_action["data"][self.pending_field] = prompt
      self.pending_field = None

      # Check again if any more fields are missing
      expected_fields = self._get_required_fields(
        self.pending_action["endpoint"],
        self.pending_action["method"]
      )
      missing = [f for f in expected_fields if not self.pending_action["data"].get(f)]

      if missing:
        self.pending_field = missing[0]
        # self.messages.append({'role': 'assistant', 'content': f"Please provide the {self.pending_field}"})
        return f"Please provide the {self.pending_field}"
      else:
        result = self.executor.execute_action(self.pending_action)
        self.pending_action = None
        return result

    # Add user message to the chat hsitory
    self.messages.append({'role': 'user', 'content': prompt})
    
    # Send the full message history to the model
    response = ollama.chat(model=self.model, messages=self.messages)

    # Extract and store the assistant's reply
    assistant_reply = response['message']['content']
    self.messages.append({'role': 'assistant', 'content': assistant_reply})
    try:
      action = json.loads(assistant_reply)

      if action.get("action") == "call_api":
        # Validate required fields before executing
        required_fields = self._get_required_fields(action["endpoint"], action["method"])
        missing = [f for f in required_fields if not action["data"].get(f)]
        if missing:
            # Save state to continue
            self.pending_action = action
            self.pending_field = missing[0]
            return f"Please provide the {self.pending_field}"
        
        api_result = self.executor.execute_action(action)
        return api_result


      elif action.get("action") == "ask_user":
        # Save pending action and field
        self.pending_action = action["pending_action"]
        self.pending_field = self._extract_missing_field(action["message"])
        return action["message"]

      elif action.get("action") == "no_api":
        return action["message"]

      else:
        return "⚠️ Unrecognized action."
    except json.JSONDecodeError:
      return f"⚠️ Could not parse response as JSON:\n{assistant_reply}"
  def _get_required_fields(self, endpoint, method):
    for api in self.api_schema:
      if api["endpoint"] == endpoint and api["method"] == method:
        return list(api["data"].keys())
    return []

  def _extract_missing_field(self, message):
    # Simple heuristic: look for the field name in the question
    keywords = ["name", "email", "password"]
    for key in keywords:
      if key in message.lower():
        return key
    return "field"  # fallback if not detected
