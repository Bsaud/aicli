# AiCLI: Your AI Command-Line Companion

**AiCLI** is a smart command-line assistant powered by Google's Gemini AI. It acts as an intelligent layer on top of your shell, translating your plain English requests into executable commands.

Ever know _what_ you want to do in the terminal, but forget the exact command or the right syntax for its options? AiCLI bridges that gap. Just describe the task, and AiCLI will suggest the command, wait for your approval, and run it for you.

## Description

This program is a Python script that provides an interactive command-line interface (CLI). When you type a request in natural language (e.g., "find all files larger than 50MB in my home folder"), the script sends this request to the Gemini API. The AI model translates the request into a shell command (e.g., `find ~ -type f -size +50M`).

The script then displays the AI-suggested command to you. For maximum speed and safety, you can simply press **Enter** to execute it or **Esc** to cancel. The script is state-aware, meaning it can properly handle directory changes (`cd`), and it runs all other commands interactively, allowing you to respond to prompts like `[Y/n]` or enter passwords.

## ✨ Features

-   **Natural Language to Command:** Translate plain English into precise shell commands.
    
-   **Safety First:** No command is ever run automatically. AiCLI always presents the command for your approval first.
    
-   **Fast Workflow:** Press **Enter** to execute or **Esc** to cancel. No extra typing needed.
    
-   **Fully Interactive:** Commands that require user input (like `apt install`, `ssh`, or password prompts) work seamlessly.
    
-   **State-Aware `cd`:** The script correctly handles `cd` commands to change the current working directory for the session.
    
-   **Contextual Prompt:** Your input prompt always displays the current working directory, so you never lose track of where you are.
    

## 🚀 Setup and Installation

Follow these steps to get AiCLI running on your local machine.

### Prerequisites

-   Python 3.6 or newer
    
-   `pip` (Python's package installer)
    

### 1. Get the Code and Dependencies

All the necessary code and dependencies are listed in the **"Project Files"** section below this guide.

1.  Create a new directory for your project (e.g., `mkdir aicli && cd aicli`).
    
2.  Copy the code from the `aicli.py` section below and save it in a file named `aicli.py`.
    
3.  Copy the text from the `requirements.txt` section below and save it in a file named `requirements.txt`.
    

### 2. Install Dependencies from File

Open your terminal in your project directory and run the following command to install the necessary Python libraries:

```
pip3 install -r requirements.txt

```

### 3. Get Your Gemini API Key

This program requires a free API key from Google AI Studio.

1.  Visit [aistudio.google.com](https://aistudio.google.com "null").
    
2.  Sign in with your Google account.
    
3.  Click **"Get API key"** and then **"Create API key in new project"**.
    
4.  Copy the generated key.
    

### 4. Configure the Script

Open the `aicli.py` file in a text editor and paste your API key into the `API_KEY` variable, replacing `"YOUR_API_KEY"`:

```
# Near the top of the file
API_KEY = "AIzaSy...your...actual...key...goes...here"

```

Save and close the file.

## 💻 Usage

Once set up, run the script from your terminal:

```
python3 aicli.py

```

The AiCLI prompt will appear. Just type what you want to do and follow the on-screen instructions.

```
--- AI Command Executor Initialized ---
Type what you want to do, or type 'exit' to quit.

/home/user/project > show the disk space usage for this drive
  └── AI Suggestion: df -h .
      Press ENTER to execute, ESC to cancel...

```

## 📂 Project Files

### `aicli.py`

```
import google.generativeai as genai
import subprocess
import sys
import os
import readchar # Import the new library for single-key presses

# --- Configuration ---
API_KEY = "YOUR_API_KEY"
if API_KEY == "YOUR_API_KEY":
    print("!!! ERROR: Please replace 'YOUR_API_KEY' with your actual API key. !!!")
    sys.exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
print("--- AI Command Executor Initialized ---")
print("Type what you want to do, or type 'exit' to quit.")

# --- Main Loop ---
while True:
    try:
        current_dir = os.getcwd()
        user_input = input(f"\n\033[1;34m{current_dir}\033[0m > ")
        if user_input.lower() == 'exit':
            break

        # 1. Translate English to a Shell Command
        prompt = (f"Translate the following request into a single, executable shell command for a Linux/macOS system. "
                  f"Only output the raw command and absolutely nothing else.\n\n"
                  f"Request: '{user_input}'")

        response = model.generate_content(prompt)
        command = response.text.strip()

        if command:
            print(f"  └── AI Suggestion: \033[1;33m{command}\033[0m")
            
            # --- NEW CONFIRMATION LOGIC ---
            print(f"      Press \033[1;32mENTER\033[0m to execute, \033[1;31mESC\033[0m to cancel...", end="", flush=True)
            key = readchar.readkey()
            print() # Move to the next line after keypress

            if key == readchar.key.ENTER:
                # 2. Handle 'cd' commands separately
                if command.strip().startswith('cd '):
                    try:
                        path_to_change = command.strip().split(maxsplit=1)[1]
                        expanded_path = os.path.expanduser(path_to_change)
                        os.chdir(expanded_path)
                        print(f"      --- Directory changed ---")
                    except FileNotFoundError:
                        print(f"\033[1;31mError: Directory not found: {path_to_change}\033[0m")
                    except IndexError:
                        os.chdir(os.path.expanduser("~"))
                        print(f"      --- Directory changed to home ---")
                else:
                    # 3. Execute all other commands interactively
                    print("      --- Executing (press Ctrl+C to stop) ---")
                    subprocess.run(command, shell=True)
                    print("      --- Done ---")
            else: # Any key other than Enter (including ESC) will cancel
                print("      Operation cancelled.")
        else:
            print("  └── AI did not return a command.")

    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"\033[1;31mAn unexpected error occurred: {e}\033[0m")

print("\n--- Executor Shut Down ---")

```

### `requirements.txt`

```
google-generativeai
readchar

```

## ⚠️ Disclaimer

**Warning:** Always review commands suggested by the AI before executing them. While designed for safety, executing an incorrect or malicious command can cause irreversible damage to your system. The user is solely responsible for the commands they choose to run.

## License

This project is licensed under the MIT License.
