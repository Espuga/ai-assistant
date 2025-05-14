from assistant.assistant import Assistant

def main():
  assistant = Assistant("cogito:14b")
  
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

if __name__ == "__main__":
  main()
