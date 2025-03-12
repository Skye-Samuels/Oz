# **OZ Assistant** 🧙‍♂️  
A powerful, terminal-based assistant integrating multiple microservices for enhanced user functionality.  

![OZ Home Screen](media/OZ%20Home%20Screen.png)  

---

## **📌 Overview**  
OZ Assistant is a command-line tool that allows users to:  
✅ **Search the Web** – Fetch search results from DuckDuckGo.  
✅ **Look Up Words** – Get word definitions, synonyms, and antonyms.  
✅ **Check Weather** – View current weather and forecasts.  
✅ **Manage To-Do Lists** – Add, view, complete, and delete tasks.  
✅ **Get Random Jokes** – Enjoy a joke whenever you need a break.  

OZ runs as a **main program** that communicates with four independent **microservices**.

---

## **🛠 Setup & Running Instructions**  

### **1️⃣ Prerequisites**  
Ensure you have the following installed:  
- **Python 3.8+**  
- **Flask** (_for microservices_)  
- **Requests** (_for API communication_)  

Install dependencies using:  
```bash
pip install -r requirements.txt
```

---

### **2️⃣ Running OZ & Microservices**  

1. To use OZ Assistant, start each microservice in a **separate terminal**:  

2. Then, start OZ Assistant

---

## **🔗 Microservices**  

To function correctly, OZ Assistant requires the following **microservices**:  

- **[Joke Service](https://github.com/rjmags1/joke-generator-microservice)** – Fetches random jokes.  
- **[Weather Service](https://github.com/Skye-Samuels/weather-information-microservice)** – Retrieves current weather and forecasts.  
- **[Dictionary/Thesaurus Service](https://github.com/Skye-Samuels/dictionary-thesaurus-microservice)** – Provides definitions, synonyms, and antonyms.  
- **[To-Do List Service](https://github.com/Skye-Samuels/todo-list-microservice)** – Manages tasks with add, delete, and complete functions.  

Ensure **all services are running** before using OZ.

---

## **📖 Features & Commands**  

| Command | Description |
|---------|------------|
| `search [query] [num]` | Search the web for [num] results. |
| `define [word]` | Get the definition of a word. |
| `synonyms [word]` | Fetch synonyms for a word. |
| `antonyms [word]` | Fetch antonyms for a word. |
| `weather [location]` | Get the current weather. |
| `forecast [location]` | Get a 3-day weather forecast. |
| `joke` | Get a random joke. |
| `add_task [task]` | Add a new task to your To-Do list. |
| `view_tasks` | Display all tasks. |
| `complete_task [id]` | Mark a task as completed. |
| `delete_task [id]` | Remove a task by its ID. |
| `help` | View all available commands. |
| `quit` | Exit the assistant. |

---

## **🖥 System Architecture**  
OZ Assistant is built on a **microservices architecture**, ensuring modularity and scalability.  
Each microservice operates independently and communicates with OZ via HTTP requests.  

**How it works:**  
1. OZ sends a request to a microservice.  
2. The microservice processes the request and returns a response.  
3. OZ displays the result to the user.  

Each microservice runs in a **separate process**, making the system flexible and scalable.

---

## **📜 License**  
This project is open-source and available under the **MIT License**.  

---

## **📩 Contact**  
For any questions, feel free to reach out!  

📧 **Email:** SkyeSamuels@protonmail.com
🐙 **GitHub:** [github.com/yourusername](https://github.com/yourusername)  