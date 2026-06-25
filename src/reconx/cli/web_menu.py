import sys

class WebMenu:
    @staticmethod
    def show():
        while True:
            print("\n=== Web Application Discovery ===")
            print("1. Web Inventory (URLs & Directories)")
            print("2. Endpoint Explorer (APIs)")
            print("3. Secret Center (Extracted Keys/Tokens)")
            print("4. Technology Map (Stack Info)")
            print("5. Return to Main Menu")
            
            choice = input("Select an option: ")
            
            if choice == "1":
                print("\n[+] Loading URL Inventory...")
            elif choice == "2":
                print("\n[+] Mapping Application Endpoints...")
            elif choice == "3":
                print("\n[+] Analyzing Secret Store...")
            elif choice == "4":
                print("\n[+] Loading Tech Map...")
            elif choice == "5":
                break
            else:
                print("Invalid option.")
