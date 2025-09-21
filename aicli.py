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
