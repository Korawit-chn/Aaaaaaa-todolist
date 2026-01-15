"""Main entry point for the Todo List application."""

import sys
from managers import AuthManager, TodoManager


class App:
    """Main application class for the Todo List CLI."""

    def __init__(self):
        """Initialize the application."""
        self.running = True
        self.auth_manager = AuthManager()
        self.todo_manager = TodoManager()
        self.current_user = None

    def display_pre_login_menu(self) -> None:
        """Display the pre-login menu and handle user input."""
        while self.running and not self.current_user:
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

        if self.current_user:
            self.display_main_menu()

    def login(self) -> None:
        """Handle user login."""
        print("\n--- Login ---")
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        if self.auth_manager.login(username, password):
            self.current_user = username
        else:
            input("Press Enter to try again...")

    def sign_up(self) -> None:
        """Handle user sign up."""
        print("\n--- Sign Up ---")
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        confirm_password = input("Confirm password: ").strip()

        if password != confirm_password:
            print("Error: Passwords do not match.")
            input("Press Enter to try again...")
            return

        if self.auth_manager.sign_up(username, password):
            input("Press Enter to continue...")
        else:
            input("Press Enter to try again...")

    def display_main_menu(self) -> None:
        """Display the main menu after login."""
        while self.running and self.current_user:
            print("\n" + "=" * 40)
            print(f"Main Menu - Logged in as: {self.current_user}")
            print("=" * 40)
            print("[1] View All Todos")
            print("[2] Create Todo")
            print("[3] View Todo Details")
            print("[4] Mark Todo as Completed")
            print("[5] Edit Todo")
            print("[6] Delete Todo")
            print("[7] Logout")
            print("[8] Exit")
            print("=" * 40)

            choice = input("\nEnter your choice (1-8): ").strip()

            if choice == "1":
                self.view_all_todos()
            elif choice == "2":
                self.create_todo()
            elif choice == "3":
                self.view_todo_details()
            elif choice == "4":
                self.mark_todo_completed()
            elif choice == "5":
                self.edit_todo()
            elif choice == "6":
                self.delete_todo()
            elif choice == "7":
                self.logout()
            elif choice == "8":
                self.exit_app()
            else:
                print("Invalid choice. Please enter 1-8.")

    def view_all_todos(self) -> None:
        """Display all todos for the current user."""
        print("\n--- All Your Todos ---")
        todos = self.todo_manager.get_all_todos(owner=self.current_user)

        if not todos:
            print("No todos found.")
            input("Press Enter to continue...")
            return

        print(f"\nYou have {len(todos)} todo(s):\n")
        for i, todo in enumerate(todos, 1):
            status_symbol = "✓" if todo.status.value == "COMPLETED" else "○"
            print(f"{i}. [{status_symbol}] {todo.title} (Priority: {todo.priority.value})")
            print(f"   ID: {todo.id}")
            print(f"   Status: {todo.status.value}")

        input("\nPress Enter to continue...")

    def create_todo(self) -> None:
        """Create a new todo item."""
        print("\n--- Create Todo ---")
        title = input("Enter todo title: ").strip()
        details = input("Enter todo details (or press Enter for none): ").strip()
        priority = input("Enter priority (HIGH/MID/LOW) [default: MID]: ").strip() or "MID"

        todo = self.todo_manager.create_todo(
            title=title,
            details=details,
            priority=priority,
            owner=self.current_user
        )

        if todo:
            input("Press Enter to continue...")

    def view_todo_details(self) -> None:
        """View details of a specific todo."""
        print("\n--- View Todo Details ---")
        todo_id = input("Enter todo ID: ").strip()
        todo = self.todo_manager.get_todo_by_id(todo_id)

        if not todo:
            print("Error: Todo not found.")
            input("Press Enter to continue...")
            return

        if todo.owner != self.current_user:
            print("Error: You don't have permission to view this todo.")
            input("Press Enter to continue...")
            return

        print(f"\nTodo Details:")
        print(f"  Title: {todo.title}")
        print(f"  Details: {todo.details}")
        print(f"  Priority: {todo.priority.value}")
        print(f"  Status: {todo.status.value}")
        print(f"  Owner: {todo.owner}")
        print(f"  Created: {todo.created_at}")
        print(f"  Updated: {todo.updated_at}")

        input("\nPress Enter to continue...")

    def mark_todo_completed(self) -> None:
        """Mark a todo as completed."""
        print("\n--- Mark Todo as Completed ---")
        todo_id = input("Enter todo ID: ").strip()
        todo = self.todo_manager.get_todo_by_id(todo_id)

        if not todo:
            print("Error: Todo not found.")
            input("Press Enter to continue...")
            return

        if todo.owner != self.current_user:
            print("Error: You don't have permission to modify this todo.")
            input("Press Enter to continue...")
            return

        if self.todo_manager.mark_completed(todo_id):
            input("Press Enter to continue...")

    def edit_todo(self) -> None:
        """Edit a todo item."""
        print("\n--- Edit Todo ---")
        todo_id = input("Enter todo ID: ").strip()
        todo = self.todo_manager.get_todo_by_id(todo_id)

        if not todo:
            print("Error: Todo not found.")
            input("Press Enter to continue...")
            return

        if todo.owner != self.current_user:
            print("Error: You don't have permission to edit this todo.")
            input("Press Enter to continue...")
            return

        title = input(f"Enter new title (current: {todo.title}) [press Enter to skip]: ").strip() or None
        details = input(f"Enter new details (current: {todo.details}) [press Enter to skip]: ").strip() or None
        priority = input(f"Enter new priority (current: {todo.priority.value}) [press Enter to skip]: ").strip() or None

        updates = {}
        if title:
            updates["title"] = title
        if details:
            updates["details"] = details
        if priority:
            updates["priority"] = priority

        if updates:
            if self.todo_manager.update_todo(todo_id, **updates):
                input("Press Enter to continue...")
        else:
            print("No changes made.")
            input("Press Enter to continue...")

    def delete_todo(self) -> None:
        """Delete a todo item."""
        print("\n--- Delete Todo ---")
        todo_id = input("Enter todo ID: ").strip()
        todo = self.todo_manager.get_todo_by_id(todo_id)

        if not todo:
            print("Error: Todo not found.")
            input("Press Enter to continue...")
            return

        if todo.owner != self.current_user:
            print("Error: You don't have permission to delete this todo.")
            input("Press Enter to continue...")
            return

        confirm = input(f"Are you sure you want to delete '{todo.title}'? (y/n): ").strip().lower()
        if confirm == "y":
            if self.todo_manager.delete_todo(todo_id):
                input("Press Enter to continue...")
        else:
            print("Delete cancelled.")
            input("Press Enter to continue...")

    def logout(self) -> None:
        """Logout the current user."""
        print(f"\nLogging out {self.current_user}...")
        self.current_user = None
        print("You have been logged out.")

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
