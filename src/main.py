"""Main entry point for the Todo List application."""

import sys


class App:
    """Main application class for the Todo List CLI."""

    def __init__(self):
        """Initialize the application."""
        self.running = True

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
        # TODO: Implement login logic with AuthManager
        print("Login feature coming soon!")

    def sign_up(self) -> None:
        """Handle user sign up."""
        print("\n--- Sign Up ---")
        # TODO: Implement sign up logic with AuthManager
        print("Sign up feature coming soon!")

    def exit_app(self) -> None:
        """Exit the application."""
        print("\nThank you for using Todo List Application. Goodbye!")
        self.running = False
        sys.exit(0)

    def run(self) -> None:
        """Start the main application loop."""
        self.display_pre_login_menu()


def main() -> None:
    """Application entry point."""
    app = App()
    app.run()


if __name__ == "__main__":
    main()
