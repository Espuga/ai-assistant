# 🤖 AI Assistant with API Integration

This project is an intelligent assistant built in Python that connects to RESTful APIs and performs actions based on natural language input. It uses [Ollama](https://ollama.com) to run a local language model (like `cogito:14b`) and can execute functions by calling defined API endpoints.

---

## 📂 Project Structure

```
.
├── main.py # Entry point to run the assistant
├── requirements.txt # Python dependencies
├── README.md # Project documentation
├── LICENSE # Project license
├── .gitignore # Git ignore rules

├── api-test/
│ └── api_test.py # Mock API server for testing

└── assistant/
├── init.py
├── assistant.py # Core Assistant logic (LLM + Tool Calling)
└── api_executor.py # Executes HTTP requests based on tool calls
```

---

## 🧠 How It Works

1. **User inputs a natural language prompt.**
2. **Assistant** parses the input and checks if it matches any available API tools (endpoints).
3. If it matches:
   - It builds the API request.
   - If required fields are missing, it asks the user for them.
   - Once all data is available, it executes the request and returns the result.
4. If it doesn’t match any known tool, the assistant replies with:  
   `"I can't do it, Sorry!"`

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/Espuga/ai-assistant.git
cd ai-assistant
```

### 2. Install Requirements

Make sure you have Python 3.8+ and [Ollama](https://ollama.com) installed and running locally.

```bash
pip install -r requirements.txt
```

> ⚠️ Note: You need to have the cogito:14b model available in Ollama. If you haven’t downloaded it yet:

```bash
ollama run cogito:14b
```

This command will download and run the model if it’s not already installed.

### 3. Run the Mock API Server

Start the test API server provided in the `api-test` folder:

```bash
python api-test/api_test.py
```

It will launch a Flask server at: `http://localhost:5000`

### 4. Start the Assistant

```bash
python main.py
```

Then type in commands like:

```text
You: Create a user with name John and email john@example.com
```

---

## 🔧 Available API Endpoints

These are mock endpoints defined in `api_executor.py`:

| Endpoint          | Method | Description           |
| ----------------- | ------ | --------------------- |
| `/users`          | POST   | Create a new user     |
| `/users/<userId>` | DELETE | Delete a user by ID   |
| `/users/<userId>` | GET    | Retrieve user details |

---

## 🛠️ Tools Logic

The assistant dynamically builds tool functions from the API schema. It uses structured function calling via `ollama.chat()` to trigger these actions based on user intent.

If the model suggests a tool call and misses required fields, it will ask the user one by one until all required parameters are gathered.

---

## 🧪 Example Prompts

```text
You: Create a user
Assistant: Please provide the name
You: Alice
Assistant: Please provide the email
You: alice@example.com
Assistant: Please provide the password
You: secure123
Assistant: {"message": "User created successfully", ...}
```

---

## 📄 License

This project is licensed under the MIT License.
