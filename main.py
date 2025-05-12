from assistant.assistant import Assistant
from assistant.assistant_v2 import Assistant_v2

def main():
  assistant = Assistant()

  print("Assistant is running. Type 'exit' to quit.\n")
  
  try:
    while True:
      user_input = input("You: ").strip()
      if user_input.lower() in ("exit", "quit"):
        print("Exiting assistant. Goodbye!")
        break

      response = assistant.send_prompt(user_input)
      print(f"Assistant: {response}\n")

  except KeyboardInterrupt:
    print("\nInterrupted by user. Exiting...")

def main_v2():
  assistant = Assistant_v2("cogito:14b")
  
  print("Assistant V2 is running. Type 'exit' to quit.\n")
  
  try:
    while True:
      user_input = input("You: ").strip()
      if user_input.lower() in ("exit", "quit"):
        print("Exiting assistant. Goodbye!")
        break

      response = assistant.send_prompt(user_input)
      print(f"Assistant: {response}\n")

  except KeyboardInterrupt:
    print("\nInterrupted by user. Exiting...")

if __name__ == "__main__":
  # main()
  main_v2()
