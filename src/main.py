"""Main entry point for the Todo List application."""

import sys
from managers import AuthManager, TodoManager
from models import Priority, Status


class App:
    """Main application class for the Todo List CLI."""

    def __init__(self):
        """Initialize the application."""
        self.running = True
        self.auth_manager = AuthManager()
        self.todo_manager = TodoManager()
        self.current_user: str | None = None

    def display_pre_login_menu(self) -> None:
        """Display the pre-login menu and handle user input."""
        while self.running and self.current_user is None:
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
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if self.auth_manager.login(username, password):
            self.current_user = username
            print(f"\nWelcome, {username}!")
            self.display_post_login_menu()
        else:
            print("Invalid username or password.")

    def sign_up(self) -> None:
        """Handle user sign up."""
        print("\n--- Sign Up ---")
        username = input("Username: ").strip()

        if not username:
            print("Username cannot be empty.")
            return

        if self.auth_manager.user_exists(username):
            print("Username already exists.")
            return

        password = input("Password: ").strip()
        if not password:
            print("Password cannot be empty.")
            return

        if self.auth_manager.sign_up(username, password):
            print("Sign up successful! You can now login.")
        else:
            print("Sign up failed.")

    def display_post_login_menu(self) -> None:
        """Display the post-login menu and handle user input."""
        while self.running and self.current_user:
            print("\n" + "=" * 40)
            print(f"Todo List - {self.current_user}")
            print("=" * 40)
            print("[1] Create a new todo")
            print("[2] View my todos")
            print("[3] Edit a todo")
            print("[4] Mark todo as completed")
            print("[5] Delete a todo")
            print("[6] Logout")
            print("[7] Mark as Completed (by ID)")
            print("[8] View todo details (by ID)")
            print("=" * 40)

            choice = input("\nEnter your choice (1-7): ").strip()

            if choice == "1":
                self.create_todo()
            elif choice == "2":
                self.view_todos()
            elif choice == "3":
                self.edit_todo()
            elif choice == "4":
                self.mark_completed()
            elif choice == "5":
                self.delete_todo()
            elif choice == "6":
                self.logout()
            elif choice == "7":
                self.mark_completed_by_id()
            elif choice == "8":
                self.view_todo_details()
            else:
                print("Invalid choice. Please enter 1-7.")

    def create_todo(self) -> None:
        """Create a new todo item."""
        print("\n--- Create New Todo ---")
        title = input("Title: ").strip()
        if not title:
            print("Title cannot be empty.")
            return

        details = input("Details: ").strip()

        print("\nPriority levels:")
        print("[1] HIGH")
        print("[2] MID")
        print("[3] LOW")
        priority_choice = input("Select priority (1-3): ").strip()

        priority_map = {"1": Priority.HIGH, "2": Priority.MID, "3": Priority.LOW}
        priority = priority_map.get(priority_choice, Priority.MID)

        todo = self.todo_manager.create_todo(
            title=title,
            details=details,
            priority=priority,
            owner=self.current_user,
        )
        print(f"\nTodo created successfully! (ID: {todo.id})")

    def view_todos(self) -> None:
        """View all todos for the current user."""
        print("\n--- My Todos ---")
        todos = self.todo_manager.get_todos_by_owner(self.current_user)

        if not todos:
            print("You have no todos.")
            return

        for idx, todo in enumerate(todos, 1):
            print(f"\n{idx}. [{todo.status.value}] {todo.title} (Priority: {todo.priority.value})")
            print(f"   ID: {todo.id}")
            print(f"   Details: {todo.details}")
            print(f"   Created: {todo.created_at}")
            print(f"   Updated: {todo.updated_at}")

    def edit_todo(self) -> None:
        """Edit an existing todo item."""
        print("\n--- Edit Todo ---")
        todos = self.todo_manager.get_todos_by_owner(self.current_user)

        if not todos:
            print("You have no todos to edit.")
            return

        print("\nYour todos:")
        for idx, todo in enumerate(todos, 1):
            print(f"{idx}. [{todo.status.value}] {todo.title}")

        try:
            choice = int(input("\nSelect todo to edit (number): ").strip())
            if choice < 1 or choice > len(todos):
                print("Invalid choice.")
                return
            selected_todo = todos[choice - 1]
        except ValueError:
            print("Invalid input.")
            return

        print(f"\nEditing: {selected_todo.title}")
        print("[1] Edit title")
        print("[2] Edit details")
        print("[3] Edit priority")
        print("[4] Cancel")

        edit_choice = input("Select option (1-4): ").strip()

        if edit_choice == "1":
            new_title = input("New title: ").strip()
            if new_title:
                selected_todo.title = new_title
                self.todo_manager.update_todo(selected_todo)
                print("Title updated!")
        elif edit_choice == "2":
            new_details = input("New details: ").strip()
            selected_todo.details = new_details
            self.todo_manager.update_todo(selected_todo)
            print("Details updated!")
        elif edit_choice == "3":
            print("\nPriority levels:")
            print("[1] HIGH")
            print("[2] MID")
            print("[3] LOW")
            priority_choice = input("Select new priority (1-3): ").strip()
            priority_map = {"1": Priority.HIGH, "2": Priority.MID, "3": Priority.LOW}
            if priority_choice in priority_map:
                selected_todo.priority = priority_map[priority_choice]
                self.todo_manager.update_todo(selected_todo)
                print("Priority updated!")
        elif edit_choice == "4":
            print("Edit cancelled.")

    def mark_completed(self) -> None:
        """Mark a todo as completed."""
        print("\n--- Mark Todo as Completed ---")
        todos = self.todo_manager.get_todos_by_owner(self.current_user)

        if not todos:
            print("You have no todos.")
            return

        print("\nYour todos:")
        for idx, todo in enumerate(todos, 1):
            print(f"{idx}. [{todo.status.value}] {todo.title}")

        try:
            choice = int(input("\nSelect todo to mark as completed (number): ").strip())
            if choice < 1 or choice > len(todos):
                print("Invalid choice.")
                return
            selected_todo = todos[choice - 1]
            selected_todo.status = Status.COMPLETED
            self.todo_manager.update_todo(selected_todo)
            print(f"'{selected_todo.title}' marked as completed!")
        except ValueError:
            print("Invalid input.")

    def mark_completed_by_id(self) -> None:
        """Prompt for a todo ID and mark it completed via the manager."""
        print("\n--- Mark Todo as Completed (by ID) ---")
        todo_id = input("Enter the todo ID to mark as completed: ").strip()
        if not todo_id:
            print("ID cannot be empty.")
            return

        success = self.todo_manager.mark_as_completed(todo_id, self.current_user)
        if success:
            print("Todo marked as completed!")
        else:
            print("Failed to mark todo as completed. Check ID and ownership.")

    def delete_todo(self) -> None:
        """Delete a todo item."""
        print("\n--- Delete Todo ---")
        todos = self.todo_manager.get_todos_by_owner(self.current_user)

        if not todos:
            print("You have no todos to delete.")
            return

        print("\nYour todos:")
        for idx, todo in enumerate(todos, 1):
            print(f"{idx}. [{todo.status.value}] {todo.title}")

        try:
            choice = int(input("\nSelect todo to delete (number): ").strip())
            if choice < 1 or choice > len(todos):
                print("Invalid choice.")
                return
            selected_todo = todos[choice - 1]
            if self.todo_manager.delete_todo(selected_todo.id):
                print(f"'{selected_todo.title}' deleted!")
            else:
                print("Failed to delete todo.")
        except ValueError:
            print("Invalid input.")

    def logout(self) -> None:
        """Logout the current user."""
        print(f"\nGoodbye, {self.current_user}!")
        self.current_user = None

    def view_all_todos(self) -> None:
        """View all todos across all users."""
        print("\n--- All Todos ---")
        todos = self.todo_manager.get_all_todos()

        if not todos:
            print("No todos found.")
            return

        for idx, todo in enumerate(todos, 1):
            print(f"\n{idx}. [{todo.status.value}] {todo.title} (Priority: {todo.priority.value})")
            print(f"   ID: {todo.id}")
            print(f"   Owner: {todo.owner}")
            print(f"   Details: {todo.details}")
            print(f"   Created: {todo.created_at}")
            print(f"   Updated: {todo.updated_at}")

    def view_todo_details(self) -> None:
        """View details for a specific todo by its ID."""
        print("\n--- Todo Details ---")
        todo_id = input("Enter the todo ID: ").strip()
        if not todo_id:
            print("ID cannot be empty.")
            return

        todo = self.todo_manager.get_todo_by_id(todo_id)
        if not todo:
            print("Todo not found.")
            return

        print(f"\nTitle: {todo.title}")
        print(f"Details: {todo.details}")
        print(f"Priority: {todo.priority.value}")
        print(f"Status: {todo.status.value}")
        print(f"Owner: {todo.owner}")
        print(f"Created: {todo.created_at}")
        print(f"Updated: {todo.updated_at}")

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
