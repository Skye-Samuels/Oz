import os
import sys
import requests
from bs4 import BeautifulSoup
import urllib.parse
import webbrowser

previous_command = ""
search_history = []


def clear_screen():

    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():

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
    ║                  WELCOME TO OZ ASSISTANT                                 ║
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
    ║                              HELP MENU                                   ║
    ╚══════════════════════════════════════════════════════════════════════════╝

       Oz Assistant is a text-based search tool for quick information access.   

    ────────────────────────────────────────────────────────────────────────────
                                   COMMANDS
    ────────────────────────────────────────────────────────────────────────────
    • help (or '?') : View available commands.

    • search [query] [num] : Search the web.
             [query] : The search term (e.g., "Python programming").
                     [num] : Number of results (max 10, default 5).
    
    • history : View your past searches.

    • open [number] : Open a past search result.
           [number] : The result index from history (e.g., "open 2").

    • define [word] : Get the definition of a word.
             [word] : Any valid English word.

    • synonyms [word] : Get synonyms for a word.
               [word] : Any valid English word.

    • antonyms [word] : Get antonyms for a word.
               [word] : Any valid English word.

    • joke : Get a random joke.

    • weather [location] : Get the current weather.
              [location] : City or region name (e.g., "New York").

    • forecast [location] : Get a 3-day weather forecast.
               [location] : City or region name (e.g., "Los Angeles").

    • back : Repeat the last command.

    • exit (or 'q') : Close the application.

    ────────────────────────────────────────────────────────────────────────────
    PRIVACY NOTICE:
    • Oz Assistant does NOT store search history beyond the current session.

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

    search_url = f"https://www.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
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
            print(f"    {idx}. {query}")
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

    joke_url = "http://localhost:8008/getRandomJoke"

    try:
        response = requests.get(joke_url, timeout=5)
        response.raise_for_status()

        joke_data = response.json()
        setup = joke_data.get("setup", "No setup available.")
        punchline = joke_data.get("punchline", "No punchline available.")

        print(f"    🤡 {setup}\n")
        print(f"    😂 {punchline}")

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
    base_url = "http://localhost:8009"
    endpoint = "/forecast" if forecast else "/current_weather"
    url = f"{base_url}{endpoint}?location={urllib.parse.quote(location)}"

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
        print("    ║                            🌎 CURRENT WEATHER                           ║")
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

    base_url = "http://localhost:8010/define"
    url = f"{base_url}/{word}"

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

    base_url = "http://localhost:8010/synonyms"
    url = f"{base_url}/{word}"

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

    base_url = "http://localhost:8010/antonyms"
    url = f"{base_url}/{word}"

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


def show_main_menu():

    clear_screen()
    
    print_banner()

    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                              MAIN MENU                                   ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    
    Welcome to Oz! Your personal assistant for fast information retrieval.

    ────────────────────────────────────────────────────────────────────────────
                              AVAILABLE COMMANDS
    ────────────────────────────────────────────────────────────────────────────
    
    • Type 'help' (or '?')        ─ View instructions and available commands.
    • Type 'search [query] [num]' ─ Search the web for [num] search results.
    • Type 'history'              ─ View your search history.
    • Type 'open [number]'        ─ Simulate opening a link.
    • Type 'define [word]'        ─ Get the definition of a word.
    • Type 'synonyms [word]'      ─ Get synonyms for a word.
    • Type 'antonyms [word]'      ─ Get antonyms for a word.
    • Type 'joke'                 ─ Get a random joke from an external service.
    • Type 'weather [location]'   ─ Get the current weather for a location.
    • Type 'forecast [location]'  ─ Get a 3-day weather forecast.
    • Type 'back'                 ─ Repeat the last command.
    • Type 'exit' (or 'q')        ─ Close the application.

    ╔══════════════════════════════════════════════════════════════════════════╗
    ║ Type your command below:                                                 ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """)


def handle_command(user_input):

    global previous_command

    if user_input == "help" or user_input == "?":
        display_help()
    elif user_input.startswith("search "):
        previous_command = user_input
        parts = user_input.split(" ")
        search_query = " ".join(parts[1:])
        num_results = 5
        if search_query.split()[-1].isdigit():
            num_results = int(search_query.split()[-1])
            search_query = " ".join(search_query.split()[:-1])
        search_web(search_query, num_results)
    elif user_input == "back":
        if previous_command and previous_command != "back":
            handle_command(previous_command)
        else:
            input("    ⚠️ No previous command to repeat.")
    elif user_input == "history":
        show_history()
    elif user_input.startswith("open "):
        number = user_input.split()[1]
        open_link(number)
    elif user_input == "joke":
        fetch_random_joke()
    elif user_input.startswith("weather "):
        location = user_input.split(" ", 1)[1] if len(user_input.split(" ", 1)) > 1 else ""
        if location:
            fetch_current_weather(location)
        else:
            input("    ⚠️ Please specify a location. Example: weather London")
    elif user_input.startswith("forecast "):
        location = user_input.split(" ", 1)[1] if len(user_input.split(" ", 1)) > 1 else ""
        if location:
            fetch_weather_forecast(location)
        else:
            input("    ⚠️ Please specify a location. Example: forecast London")
    elif user_input.startswith("define "):
        word = user_input.split(" ", 1)[1] if len(user_input.split(" ", 1)) > 1 else ""
        if word:
            define_word(word)
        else:
            input("    ⚠️ Please specify a word. Example: define test")
    elif user_input.startswith("synonyms "):
        word = user_input.split(" ", 1)[1] if len(user_input.split(" ", 1)) > 1 else ""
        if word:
            get_synonyms(word)
        else:
            input("    ⚠️ Please specify a word. Example: synonyms happy")
    elif user_input.startswith("antonyms "):
        word = user_input.split(" ", 1)[1] if len(user_input.split(" ", 1)) > 1 else ""
        if word:
            get_antonyms(word)
        else:
            input("    ⚠️ Please specify a word. Example: antonyms good")
    elif user_input == "exit" or user_input == "q":
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
