"""Main entry point for the Todo List application."""

import sys
from auth import AuthManager


class App:
    """Main application class for the Todo List CLI."""

    def __init__(self):
        """Initialize the application."""
        self.running = True
        self.auth_manager = AuthManager("users.json")
        self.current_user = None

    def display_pre_login_menu(self) -> None:
        """Display the pre-login menu and handle user input."""
        while self.running:
            print("\n" + "=" * 40)
            print("Welcome to Todo List Application")
            print("=" * 40)
            print("[1] Login")
            print("[2] Sign Up")
            print("[3] Exit")
            print("=" * 40)

            choice = input("\nEnter your choice (1-3): ").strip()

            if choice == "1":
                self.login()
            elif choice == "2":
                self.sign_up()
            elif choice == "3":
                self.exit_app()
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    def login(self) -> None:
        """Handle user login."""
        print("\n--- Login ---")
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        
        success, message = self.auth_manager.login(username, password)
        
        if success:
            self.current_user = username
            print(f"\n✓ {message}")
            self.main_app_menu()
        else:
            print(f"\n✗ {message}")

    def sign_up(self) -> None:
        """Handle user sign up."""
        print("\n--- Sign Up ---")
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        confirm_password = input("Confirm password: ").strip()
        
        if password != confirm_password:
            print("\n✗ Passwords do not match.")
            return
        
        success, message = self.auth_manager.signup(username, password)
        
        if success:
            print(f"\n✓ {message}")
            print("You can now login with your new account.")
        else:
            print(f"\n✗ {message}")

    def exit_app(self) -> None:
        """Exit the application."""
        print("\nThank you for using Todo List Application. Goodbye!")
        self.running = False
        sys.exit(0)

    def main_app_menu(self) -> None:
        """Display the main menu after user logs in."""
        print(f"\n{'='*40}")
        print(f"Main Menu - Logged in as: {self.current_user}")
        print(f"{'='*40}")
        print("[1] View todos")
        print("[2] Add todo")
        print("[3] Logout")
        print(f"{'='*40}")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            print("\nTodo view feature coming soon!")
        elif choice == "2":
            print("\nTodo creation feature coming soon!")
        elif choice == "3":
            self.logout()
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    def logout(self) -> None:
        """Handle user logout."""
        print(f"\nGoodbye, {self.current_user}!")
        self.current_user = None

    def run(self) -> None:
        """Start the main application loop."""
        self.display_pre_login_menu()


def main() -> None:
    """Application entry point."""
    app = App()
    app.run()


if __name__ == "__main__":
    main()
