import os
import sys
import requests
from bs4 import BeautifulSoup
import urllib.parse
import webbrowser
import json

WEB_BASE_URL = "https://www.duckduckgo.com"
JOKE_BASE_URL = "http://localhost:8008"
WEATHER_BASE_URL = "http://localhost:8009"
WORDS_BASE_URL = "http://localhost:8010"
TODO_BASE_URL = "http://localhost:8011"

previous_command = ""
search_history = []


def clear_screen():

    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():

    # Source: https://patorjk.com/software/taag/

    banner = '''

        ██████╗ ███████╗    ██╗  ██╗███████╗██╗     ██████╗ ███████╗██████╗ 
       ██╔═══██╗╚══███╔╝    ██║  ██║██╔════╝██║     ██╔══██╗██╔════╝██╔══██╗
       ██║   ██║  ███╔╝     ███████║█████╗  ██║     ██████╔╝█████╗  ██████╔╝
       ██║   ██║ ███╔╝      ██╔══██║██╔══╝  ██║     ██╔═══╝ ██╔══╝  ██╔══██╗
       ╚██████╔╝███████╗    ██║  ██║███████╗███████╗██║     ███████╗██║  ██║
        ╚═════╝ ╚══════╝    ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝'''
    print(banner)


def first_time_message():

    clear_screen()
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                         WELCOME TO OZ ASSISTANT                          ║
    ║                                                                          ║
    ║ ✨ "Step into the wonderful world of Oz, where knowledge meets fantasy.  ║
    ║    Whether you're searching for wisdom, truth, or just a quick answer,   ║
    ║    your journey begins here."                                            ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """)
    input("    🌟 Press Enter to begin your journey... ")


def display_help():

    global previous_command

    previous_command = "help"

    clear_screen()
    print_banner()
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                              📖 HELP MENU 📖                             ║
    ╚══════════════════════════════════════════════════════════════════════════╝

      ✨ Oz Assistant is a text-based search tool for quick information access.   

    ────────────────────────────────────────────────────────────────────────────
                               🔍 SEARCH COMMANDS
    ────────────────────────────────────────────────────────────────────────────
      🆘  • help (or '?')                 
           - View available commands.
      
      🔍  • search [query] [num]          
           - Search the web using a query.
           - [query]: The search term (e.g., "Python programming").
           - [num]: Number of results (max 10, default 5).

      🕒  • history                       
           - View your past searches.
      
      🌍  • open [number]                 
           - Open a past search result.
           - [number]: The index of a search result from history (e.g., "open 2").

    ────────────────────────────────────────────────────────────────────────────
                               📖 DICTIONARY COMMANDS
    ────────────────────────────────────────────────────────────────────────────
      📖  • define [word]                 
           - Get the definition of a word.
           - [word]: Any valid English word.

      🔄  • synonyms [word]               
           - Get synonyms for a word.
           - [word]: Any valid English word.

      🚫  • antonyms [word]               
           - Get antonyms for a word.
           - [word]: Any valid English word.

    ────────────────────────────────────────────────────────────────────────────
                                  🎭 FUN COMMANDS
    ────────────────────────────────────────────────────────────────────────────
      😂  • joke                          
           - Get a random joke.

    ────────────────────────────────────────────────────────────────────────────
                                 🌦 WEATHER COMMANDS
    ────────────────────────────────────────────────────────────────────────────
      🌦  • weather [location]            
           - Get the current weather for a location.
           - [location]: City or region name (e.g., "New York").

      📅  • forecast [location]           
           - Get a 3-day weather forecast.
           - [location]: City or region name (e.g., "Los Angeles").

    ────────────────────────────────────────────────────────────────────────────
                               📋 TO-DO LIST COMMANDS
    ────────────────────────────────────────────────────────────────────────────
      📋  • view_tasks                    
           - Display your To-Do list.

      ➕  • add_task [task]               
           - Add a new task to your To-Do list.
           - [task]: Description of the task (e.g., "Buy groceries").

      ✅  • complete_task [number]        
           - Mark a task as completed.
           - [number]: The ID of the task to complete (e.g., "complete_task 3").

      ❌  • delete_task [number]          
           - Remove a task by its ID.
           - [number]: The ID of the task to remove (e.g., "delete_task 2").

      🔥  • delete_all_tasks              
           - Remove all tasks from the To-Do list.

    ────────────────────────────────────────────────────────────────────────────
                               ⚙️ SYSTEM COMMANDS
    ────────────────────────────────────────────────────────────────────────────
      🆘  • help (or '?')                 
           - View this help menu.

      ⏪  • back                          
           - Repeat the last command.

      🚪  • quit (or 'q')                 
           - Close the application.

    ────────────────────────────────────────────────────────────────────────────
                               🔒 PRIVACY NOTICE
    ────────────────────────────────────────────────────────────────────────────

      ⚠️  Oz Assistant   DOES NOT   store search history beyond the current session.
      ⚠️  Oz Assistant   DOES   store to-do list items between sessions.

    ╔══════════════════════════════════════════════════════════════════════════╗
    ║ Press Enter to return to the main menu...                                ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """)
    input()


def search_web(query, num_results=5):

    global previous_command
    num_results = min(num_results, 10)
    previous_command = f"search {query} {num_results}".strip()

    clear_screen()
    print_banner()
    print(f"\n    🔍 Searching for: {query} (Top {num_results} results)...\n")

    if query not in search_history:
        search_history.append(query)

    search_url = f"{WEB_BASE_URL}/html/?q={urllib.parse.quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        for idx, result in enumerate(soup.select(".result__title")[:num_results]):
            title = result.get_text(strip=True)
            raw_link = result.a["href"] if result.a else None

            if raw_link and "uddg=" in raw_link:
                cleaned_link = urllib.parse.parse_qs(urllib.parse.urlparse(raw_link).query).get("uddg", ["No Link"])[0]
            else:
                cleaned_link = raw_link or "No Link"

            results.append((title, cleaned_link))

        if not results:
            print("    ❌ No results found.")
        else:
            print("    ╔══════════════════════════════════════════════════════════════════════════╗")
            print("    ║                             SEARCH RESULTS                               ║")
            print("    ╚══════════════════════════════════════════════════════════════════════════╝\n")
            for i, (title, link) in enumerate(results, start=1):
                print(f"    🔹 {i}. {title}\n       🔗 Visit: {link}\n")

    except requests.RequestException as e:
        print(f"    ❌ Error fetching search results: {e}")

    input('''
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║ Press Enter to return to the main menu...                                ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    ''')


def show_history():

    global previous_command
    previous_command = "history"
    clear_screen()
    print_banner()
    if not search_history:
        print("\n    🕒 No search history available.\n")
    else:
        print("\n    🔍 Search History:\n")
        for idx, query in enumerate(search_history, 1):
            print(f"      {idx}. {query}")
    input('''
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║ Press Enter to return to the main menu...                                ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    ''')


def open_link(number):

    try:
        idx = int(number) - 1
        if 0 <= idx < len(search_history):
            query = search_history[idx]
            print(f"    🔍 Re-searching for: {query}")
            search_web(query)
        else:
            input("    ⚠️ Invalid link number.")
    except (ValueError, IndexError):
        input("    ⚠️ Please enter a valid number.")


def fetch_random_joke():

    global previous_command
    previous_command = "joke"

    clear_screen()
    print_banner()
    print("\n    🎭 Fetching a random joke...\n")

    joke_url = f"{JOKE_BASE_URL}/getRandomJoke"

    try:
        response = requests.get(joke_url, timeout=5)
        response.raise_for_status()

        joke_data = response.json()
        setup = joke_data.get("setup", "No setup available.")
        punchline = joke_data.get("punchline", "No punchline available.")

        print(f"    🤡 {setup.replace("\n", "      \n")}\n")
        print(f"    😂 {punchline.replace("\n", "      \n")}")

    except requests.exceptions.ConnectionError:
        print("    ❌ Unable to connect to the joke server.")
        print("    🔹 Please ensure the joke microservice is running on port 8008.")

    except requests.exceptions.Timeout:
        print("    ❌ The request timed out.")
        print("    🔹 The joke server is taking too long to respond. Try again later.")

    except requests.exceptions.HTTPError as http_err:
        print(f"    ❌ HTTP Error: {http_err}")
        print("    🔹 The joke service might be experiencing issues.")

    except requests.RequestException as e:
        print(f"    ❌ An unexpected error occurred: {e}")
        print("    🔹 Please check your internet connection or try again later.")

    input('''
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║ Press Enter to return to the main menu...                                ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    ''')


def fetch_weather_data(location, forecast=False):

    endpoint = "/forecast" if forecast else "/current_weather"
    url = f"{WEATHER_BASE_URL}{endpoint}?location={urllib.parse.quote(location)}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        return {"error": "Unable to connect to the weather server. Ensure the weather microservice is running on port 8009."}

    except requests.exceptions.Timeout:
        return {"error": "The request to the weather server timed out. Try again later."}

    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP Error: {http_err}"}

    except requests.RequestException as e:
        return {"error": f"An unexpected error occurred: {e}"}


def fetch_current_weather(location):

    global previous_command

    previous_command = f"weather {location}"

    clear_screen()
    print_banner()

    if not location.strip():
        print("\n    ❌ Error: Location cannot be empty.")
        input("\n    🔹 Press Enter to return to the main menu...")
        return

    print(f"\n    ⏳ Gathering weather insights for {location}...\n")
    weather_data = fetch_weather_data(location)

    if "error" in weather_data:
        print(f"\n    ❌ {weather_data['error']}")
    else:
        weather_icon = get_weather_icon(weather_data["weather_condition"])
        print("    ╔══════════════════════════════════════════════════════════════════════════╗")
        print("    ║                            🌎 CURRENT WEATHER                            ║")
        print("    ╚══════════════════════════════════════════════════════════════════════════╝")
        print(f"    📍 Location: {weather_data['location']}")
        print(f"    {weather_icon}")
        print(f"    🌡 Temperature: {weather_data['temperature_C']}°C / {weather_data['temperature_F']}°F")
        print(f"    💧 Humidity: {weather_data['humidity']}%")
        print(f"    ⛅ Condition: {weather_data['weather_condition']}")
        print("    ═══════════════════════════════════════════════════════════════════════════")

    input('''
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║ Press Enter to return to the main menu...                                ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    ''')


def fetch_current_weather(location):

    global previous_command

    previous_command = f"weather {location}"

    clear_screen()
    print_banner()

    if not location.strip():
        print("\n    ❌ Error: Location cannot be empty.")
        input("\n    🔹 Press Enter to return to the main menu...")
        return

    print(f"\n    ⏳ Retrieving current weather for {location}...\n")
    weather_data = fetch_weather_data(location)

    if "error" in weather_data:
        print(f"\n    ❌ {weather_data['error']}")
    else:
        print("    ╔══════════════════════════════════════════════════════════════════════════╗")
        print("    ║                          🌎 CURRENT WEATHER                              ║")
        print("    ╚══════════════════════════════════════════════════════════════════════════╝\n")
        print(f"    📍 Location: {weather_data['location']}")
        print(f"    🌡 Temperature: {weather_data['temperature_C']}°C / {weather_data['temperature_F']}°F")
        print(f"    💧 Humidity: {weather_data['humidity']}%")
        print(f"    ⛅ Condition: {weather_data['weather_condition']}")

    input('''
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║ Press Enter to return to the main menu...                                ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    ''')


def fetch_weather_forecast(location):

    global previous_command

    previous_command = f"forecast {location}"

    clear_screen()
    print_banner()

    if not location.strip():
        print("\n    ❌ Error: Location cannot be empty.")
        input("\n    🔹 Press Enter to return to the main menu...")
        return

    print(f"\n    ⏳ Fetching 3-day forecast for {location}...\n")
    forecast_data = fetch_weather_data(location, forecast=True)

    if "error" in forecast_data:
        print(f"\n    ❌ {forecast_data['error']}")
    else:
        print("    ╔══════════════════════════════════════════════════════════════════════════╗")
        print("    ║                         📅 3-DAY WEATHER FORECAST                        ║")
        print("    ╚══════════════════════════════════════════════════════════════════════════╝\n")
        print(f"    📍 Location: {forecast_data['location']}")

        for day in forecast_data["forecast"]:
            print("\n    ───────────────────────────────────────────────────────────────────────────\n")
            print(f"    📅 Date: {day['date']}")
            print(f"    🌡 Max Temp: {day['temperature_max_C']}°C / {day['temperature_max_F']}°F")
            print(f"    🌡 Min Temp: {day['temperature_min_C']}°C / {day['temperature_min_F']}°F")
            print(f"    ⛅ Condition: {day['weather_condition']}")

    input('''
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║ Press Enter to return to the main menu...                                ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    ''')


def fetch_word_definition(word):

    definition_url = f"{WORDS_BASE_URL}/define"
    url = f"{definition_url}/{word}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Unable to connect to the dictionary service. Ensure it is running on port 8010."}
    except requests.exceptions.Timeout:
        return {"error": "The request to the dictionary service timed out. Try again later."}
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP Error: {http_err}"}
    except requests.RequestException as e:
        return {"error": f"An unexpected error occurred: {e}"}


def fetch_word_synonyms(word):

    synonyms_url = f"{WORDS_BASE_URL}/synonyms"
    url = f"{synonyms_url}/{word}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Unable to connect to the dictionary service. Ensure it is running on port 8010."}
    except requests.exceptions.Timeout:
        return {"error": "The request to the dictionary service timed out. Try again later."}
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP Error: {http_err}"}
    except requests.RequestException as e:
        return {"error": f"An unexpected error occurred: {e}"}


def fetch_word_antonyms(word):

    antonyms_url = f"{WORDS_BASE_URL}/antonyms"
    url = f"{antonyms_url}/{word}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Unable to connect to the dictionary service. Ensure it is running on port 8010."}
    except requests.exceptions.Timeout:
        return {"error": "The request to the dictionary service timed out. Try again later."}
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP Error: {http_err}"}
    except requests.RequestException as e:
        return {"error": f"An unexpected error occurred: {e}"}


def define_word(word):

    global previous_command

    previous_command = f"define {word}"

    clear_screen()
    print_banner()

    if not word.strip():
        print("\n    ❌ Error: Word cannot be empty.\n")
        input("    🔹 Press Enter to return to the main menu...")
        return

    print(f"\n    ⏳ Fetching definition for: {word}...\n")

    definition_data = fetch_word_definition(word)

    if "error" in definition_data:
        print(f"\n    ❌ {definition_data['error']}\n")
    else:
        print("    ╔══════════════════════════════════════════════════════════════════════════╗")
        print("    ║                          📖 WORD DEFINITION                              ║")
        print("    ╚══════════════════════════════════════════════════════════════════════════╝\n")
        print(f"    📝 Word: {definition_data['word']}\n")

        displayed = 0
        for meaning in definition_data["meanings"]:
            if displayed >= 5:
                break

            part_of_speech = meaning["part_of_speech"].capitalize()
            definition = meaning["definition"].strip()

            if not definition or definition in [":", "-"]:
                continue  

            print(f"    🔹 {part_of_speech}: {definition}\n")

            example = meaning.get("example", "").strip()
            if example and example.lower() != "no example available":
                print(f"    ✍️  Example: {example}\n")

            displayed += 1

    input('''
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║ Press Enter to return to the main menu...                                ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    ''')


def get_synonyms(word):

    global previous_command

    previous_command = f"synonyms {word}"

    clear_screen()
    print_banner()

    if not word.strip():
        print("\n    ❌ Error: Word cannot be empty.\n")
        input("    🔹 Press Enter to return to the main menu...")
        return

    print(f"\n    ⏳ Fetching synonyms for: {word}...\n")

    synonym_data = fetch_word_synonyms(word)

    if "error" in synonym_data:
        print(f"\n    ❌ {synonym_data['error']}\n")
    else:
        print("    ╔══════════════════════════════════════════════════════════════════════════╗")
        print("    ║                            🔄 SYNONYMS LIST                              ║")
        print("    ╚══════════════════════════════════════════════════════════════════════════╝\n")
        print(f"    📝 Word: {synonym_data['word']}\n")

        synonyms = synonym_data.get("synonyms", [])
        if not synonyms or synonyms == ["No synonyms found"]:
            print("    ❌ No synonyms found.\n")
        else:
            print("    🔹 Synonyms:\n")
            for synonym in synonyms[:5]:  
                print(f"      - {synonym}")

    input('''
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║ Press Enter to return to the main menu...                                ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    ''')


def get_antonyms(word):

    global previous_command

    previous_command = f"antonyms {word}"

    clear_screen()
    print_banner()

    if not word.strip():
        print("\n    ❌ Error: Word cannot be empty.\n")
        input("    🔹 Press Enter to return to the main menu...")
        return

    print(f"\n    ⏳ Fetching antonyms for: {word}...\n")

    antonym_data = fetch_word_antonyms(word)

    if "error" in antonym_data:
        print(f"\n    ❌ {antonym_data['error']}\n")
    else:
        print("    ╔══════════════════════════════════════════════════════════════════════════╗")
        print("    ║                            🔄 ANTONYMS LIST                              ║")
        print("    ╚══════════════════════════════════════════════════════════════════════════╝\n")
        print(f"    📝 Word: {antonym_data['word']}\n")

        antonyms = antonym_data["antonyms"]
        if antonyms == ["No antonyms found"]:
            print("    ❌ No antonyms found for this word.\n")
        else:
            formatted_antonyms = ", ".join(antonyms[:10])
            print("    🔹 Antonyms:\n")
            for antonym in antonyms[:5]:  
                print(f"      - {antonym}")

    input('''
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║ Press Enter to return to the main menu...                                ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    ''')


def add_task(task):

    global previous_command

    previous_command = f"add task {task}"

    clear_screen()
    print_banner()

    if not task.strip():
        print("\n    ❌ Error: Task description cannot be empty.\n")
        input("    🔹 Press Enter to return to the main menu...")
        return

    print(f"\n    ⏳ Adding task: {task}...\n")

    try:
        response = requests.post(f"{TODO_BASE_URL}/todo/add", json={"task": task})
        response.raise_for_status()
        print("    ✅ Task added successfully!")

    except requests.exceptions.ConnectionError:
        print("    ❌ Unable to connect to the To-Do service.")
        print("    🔹 Please ensure the service is running on port 8011.")

    except requests.exceptions.Timeout:
        print("    ❌ The request timed out.")
        print("    🔹 The To-Do service is taking too long to respond. Try again later.")

    except requests.exceptions.HTTPError as http_err:
        print(f"    ❌ HTTP Error: {http_err}")
        print("    🔹 The To-Do service might be experiencing issues.")

    except requests.RequestException as e:
        print(f"    ❌ An unexpected error occurred: {e}")
        print("    🔹 Please check your connection and try again.")

    input('''
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║ Press Enter to return to the main menu...                                ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    ''')


def view_tasks():

    global previous_command

    previous_command = "view_tasks"

    clear_screen()
    print_banner()
    print("\n    ⏳ Retrieving your To-Do List...\n")

    try:
        response = requests.get(f"{TODO_BASE_URL}/todo/list", timeout=5)
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict) or "tasks" not in data:
            print("    ❌ Error: Invalid response format. Expected a dictionary with a 'tasks' key.\n")
        else:
            tasks = data["tasks"]

            print("    ╔══════════════════════════════════════════════════════════════════════════╗")
            print("    ║                               📝 TO-DO LIST                              ║")
            print("    ╚══════════════════════════════════════════════════════════════════════════╝\n")

            if not tasks:
                print("    🎉 No tasks found! You're all caught up!")
            else:
                print("    ╔═══════════╦═════════════════════════════════════════════════════╦════════╗")
                print("    ║    ID     ║                        TASK                         ║ STATUS ║")
                print("    ╠═══════════╬═════════════════════════════════════════════════════╬════════╣")

                for task in tasks:
                    task_id = f"{task['id']}".center(9)  
                    task_name = task['task'].center(51)  
                    status = "✅" if task["completed"] else "❌"
                    status = status.center(5)

                    print(f"    ║ {task_id} ║ {task_name} ║ {status} ║")

                print("    ╚═══════════╩═════════════════════════════════════════════════════╩════════╝")

    except requests.exceptions.ConnectionError:
        print("    ❌ Unable to connect to the To-Do service.")
        print("    🔹 Please ensure the service is running on port 8011.")

    except requests.exceptions.Timeout:
        print("    ❌ The request timed out.")
        print("    🔹 The To-Do service is taking too long to respond. Try again later.")

    except requests.exceptions.HTTPError as http_err:
        print(f"    ❌ HTTP Error: {http_err}")
        print("    🔹 The To-Do service might be experiencing issues.")

    except requests.RequestException as e:
        print(f"    ❌ An unexpected error occurred: {e}")
        print("    🔹 Please check your connection and try again.")
    
    input('''
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║ Press Enter to return to the main menu...                                ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    ''')


def delete_task(task_number):

    global previous_command

    previous_command = f"delete {task_number}"

    clear_screen()
    print_banner()

    if not task_number.isdigit():
        print("\n    ❌ Error: Task number must be a valid integer.\n")
        input("    🔹 Press Enter to return to the main menu...")
        return

    print(f"\n    ⏳ Removing task #{task_number}...\n")

    try:
        response = requests.delete(f"{TODO_BASE_URL}/todo/delete/{task_number}", timeout=5)
        response.raise_for_status()
        response_data = response.json()

        if "message" in response_data and "deleted" in response_data["message"].lower():
            print("    ✅ Task deleted successfully!")
        elif response_data.get("success") is True or response_data.get("message") == "Task deleted successfully":
            print("    ✅ Task deleted successfully!")
        else:
            print("    ❌ Task not found or could not be deleted.")

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"    ❌ Error: Task #{task_number} not found.")
            print("    🔹 Please check the task number and try again.")
        else:
            print(f"    ❌ HTTP Error: {http_err}")
            print("    🔹 The To-Do service might be experiencing issues.")

    except requests.exceptions.ConnectionError:
        print("    ❌ Unable to connect to the To-Do service.")
        print("    🔹 Please ensure the service is running on port 8011.")

    except requests.exceptions.Timeout:
        print("    ❌ The request timed out.")
        print("    🔹 The To-Do service is taking too long to respond. Try again later.")

    except requests.RequestException as e:
        print(f"    ❌ An unexpected error occurred: {e}")
        print("    🔹 Please check your connection and try again.")

    input('''
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║ Press Enter to return to the main menu...                                ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    ''')


def delete_all_tasks():

    global previous_command

    previous_command = "delete_all_tasks"

    clear_screen()
    print_banner()
    print("\n    ⏳ Deleting all tasks from the To-Do list...\n")

    try:
        response = requests.delete(f"{TODO_BASE_URL}/todo/delete_all", timeout=5)
        response.raise_for_status()
        response_data = response.json()

        if "message" in response_data:
            print(f"    ✅ {response_data['message']}")
        else:
            print("    ❌ Unexpected error: No confirmation message received.")

    except requests.exceptions.ConnectionError:
        print("    ❌ Unable to connect to the To-Do service.")
        print("    🔹 Please ensure the service is running on port 8011.")

    except requests.exceptions.Timeout:
        print("    ❌ The request timed out.")
        print("    🔹 The To-Do service is taking too long to respond. Try again later.")

    except requests.exceptions.HTTPError as http_err:
        print(f"    ❌ HTTP Error: {http_err}")
        print("    🔹 The To-Do service might be experiencing issues.")

    except requests.RequestException as e:
        print(f"    ❌ An unexpected error occurred: {e}")
        print("    🔹 Please check your connection and try again.")

    input('''
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║ Press Enter to return to the main menu...                                ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    ''')


def complete_task(task_number):

    global previous_command

    previous_command = f"complete_task {task_number}"

    clear_screen()
    print_banner()

    if not task_number.isdigit():
        print("\n    ❌ Error: Task number must be a valid integer.\n")
        input("    🔹 Press Enter to return to the main menu...")
        return

    print(f"\n    ⏳ Marking task #{task_number} as complete...\n")

    try:
        response = requests.put(f"{TODO_BASE_URL}/todo/complete/{task_number}", timeout=5)
        response.raise_for_status()
        response_data = response.json()

        if "message" in response_data:
            print(f"    ✅ {response_data['message']}")
        else:
            print("    ❌ Unexpected error: No confirmation message received.")

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"    ❌ Error: Task #{task_number} not found.")
            print("    🔹 Please check the task number and try again.")
        else:
            print(f"    ❌ HTTP Error: {http_err}")
            print("    🔹 The To-Do service might be experiencing issues.")

    except requests.exceptions.ConnectionError:
        print("    ❌ Unable to connect to the To-Do service.")
        print("    🔹 Please ensure the service is running on port 8011.")

    except requests.exceptions.Timeout:
        print("    ❌ The request timed out.")
        print("    🔹 The To-Do service is taking too long to respond. Try again later.")

    except requests.RequestException as e:
        print(f"    ❌ An unexpected error occurred: {e}")
        print("    🔹 Please check your connection and try again.")

    input('''
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║ Press Enter to return to the main menu...                                ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    ''')


def show_main_menu():
    
    clear_screen()
    print_banner()

    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                              🌟 MAIN MENU 🌟                             ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    
       Welcome to Oz! Your personal assistant for fast information retrieval.

    ────────────────────────────────────────────────────────────────────────────
                              📌 AVAILABLE COMMANDS
    ────────────────────────────────────────────────────────────────────────────

      🔍  Type 'search [query] [num]'   ─ Search the web for [num] results.
      🕒  Type 'history'                ─ View your search history.
      🌍  Type 'open [number]'          ─ Open a previous web search.

      📖  Type 'define [word]'          ─ Get the definition of a word.
      🔄  Type 'synonyms [word]'        ─ Get synonyms for a word.
      🚫  Type 'antonyms [word]'        ─ Get antonyms for a word.

      🎭  Type 'joke'                   ─ Get a random joke.
      
      🌦  Type 'weather [location]'     ─ Get the current weather for a location.
      📅  Type 'forecast [location]'    ─ Get a 3-day weather forecast.
  
      📋  Type 'view_tasks'             ─ Display your To-Do list.
      ➕  Type 'add_task [task]'        ─ Add a new task to your To-Do list.
      ✅  Type 'complete_task [number]' ─ Mark a task as completed.
      ❌  Type 'delete_task [number]'   ─ Remove a task by its ID number.
      🔥  Type 'delete_all_tasks'       ─ Remove all tasks from the To-Do list.

      ⏪  Type 'back'                   ─ Repeat the last command.
      ❓  Type 'help' (or '?')          ─ View commands and command arguments.
      🚪  Type 'quit' (or 'q')          ─ Close the application.
  
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║ Type your command below:                                                 ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """)


def handle_command(user_input):

    global previous_command

    if not user_input.strip():
        return

    user_input = user_input.lower()
    command, _, argument = user_input.partition(" ")

    if command in ["help", "?"]:
        display_help()

    elif command == "search":
        previous_command = user_input
        parts = argument.rsplit(" ", 1)
        num_results = 5

        if parts[-1].isdigit():
            num_results = int(parts[-1])
            search_query = " ".join(parts[:-1])
        else:
            search_query = argument

        if search_query:
            search_web(search_query, num_results)
        else:
            input("    ⚠️ Please provide a search query. Example: search Python programming 5")

    elif command == "back":
        if previous_command and previous_command != "back":
            handle_command(previous_command)
        else:
            input("    ⚠️ No previous command to repeat.")

    elif command == "history":
        show_history()

    elif command == "open":
        if argument.isdigit():
            open_link(argument)
        else:
            input("    ⚠️ Please specify a valid number. Example: open 2")

    elif command == "joke":
        fetch_random_joke()

    elif command == "weather":
        if argument:
            fetch_current_weather(argument)
        else:
            input("    ⚠️ Please specify a location. Example: weather London")

    elif command == "forecast":
        if argument:
            fetch_weather_forecast(argument)
        else:
            input("    ⚠️ Please specify a location. Example: forecast London")

    elif command == "define":
        if argument:
            define_word(argument)
        else:
            input("    ⚠️ Please specify a word. Example: define test")

    elif command == "synonyms":
        if argument:
            get_synonyms(argument)
        else:
            input("    ⚠️ Please specify a word. Example: synonyms happy")

    elif command == "antonyms":
        if argument:
            get_antonyms(argument)
        else:
            input("    ⚠️ Please specify a word. Example: antonyms good")

    elif command == "add_task":
        if argument:
            add_task(argument)
        else:
            input("    ⚠️ Please specify a task. Example: add_task Buy groceries")

    elif command == "view_tasks":
        view_tasks()

    elif command == "delete_task":

        if argument.isdigit():
            delete_task(argument)
        else:
            input("    ⚠️ Please specify a valid task number. Example: delete_task 2")

    elif command == "delete_all_tasks":
        delete_all_tasks()

    elif command == "complete_task":
        if argument.isdigit():
            complete_task(argument)
        else:
            input("    ⚠️ Please specify a valid task number. Example: complete_task 2")


    elif command in ["exit", "e", "quit", "q"]:
        confirm = input("\n    ❓ Are you sure you want to exit? (yes/no): ").strip().lower()
        if confirm in ["yes", "y"]:
            sys.exit("\n    🔹 Goodbye!\n")

    else:
        input("    ⚠️ Invalid command. Type 'help' for a list of commands.")


def main():

    first_time_message()

    while True:
        show_main_menu()
        user_input = input("    > ").strip().lower()
        if user_input:
            handle_command(user_input)


if __name__ == "__main__":
    main()
