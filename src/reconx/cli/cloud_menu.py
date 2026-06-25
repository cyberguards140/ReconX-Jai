class CloudMenu:
    @staticmethod
    def show():
        while True:
            print("\n=== Cloud Intelligence Center ===")
            print("1. Cloud Inventory (Multi-Cloud Assets)")
            print("2. Storage Explorer (S3, Blob)")
            print("3. IAM Explorer (Identities & Roles)")
            print("4. Cloud Findings & Exposures")
            print("5. Cloud Risk Center")
            print("6. Return to Main Menu")

            choice = input("Select an option: ")

            if choice == "1":
                print("\n[+] Loading Cloud Inventory...")
            elif choice == "2":
                print("\n[+] Loading Storage Explorer...")
            elif choice == "3":
                print("\n[+] Loading IAM Explorer...")
            elif choice == "4":
                print("\n[+] Loading Cloud Findings...")
            elif choice == "5":
                print("\n[+] Generating Cloud Risk Scorecard...")
            elif choice == "6":
                break
            else:
                print("Invalid option.")
