import sys

class FindingsMenu:
    @staticmethod
    def show():
        while True:
            print("\n=== Findings Center ===")
            print("1. View All Findings")
            print("2. Risk Dashboard")
            print("3. Vulnerability Queue")
            print("4. Return to Main Menu")
            
            choice = input("Select an option: ")
            
            if choice == "1":
                print("\n[+] Fetching findings...")
                # Call internal engine logic here
            elif choice == "2":
                print("\n[+] Loading Risk Dashboard...")
            elif choice == "3":
                print("\n[+] Loading Vuln Queue...")
            elif choice == "4":
                break
            else:
                print("Invalid option.")
