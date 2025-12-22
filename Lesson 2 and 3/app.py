import sys
from getpass import getpass
from google.genai import Client
from dotenv import load_dotenv
from google.genai.types import Content, Part

from database.operations import (
    register_user,
    login_user,
    get_or_create_active_conversation,
    save_message,
    load_history,
    get_user_conversations,
    create_conversation,
    DuplicateUser,
    UserNotFound,
)

load_dotenv()


class Agent:
    def __init__(self, user_id: int, conversation_id: int = None):
        self.user_id = user_id
        if conversation_id:
            self.conversation_id = conversation_id
        else:
            self.conversation_id = get_or_create_active_conversation(user_id)
        self.client = Client()
        history = self._load_and_format_history()

        self.chat = self.client.chats.create(model="gemini-2.5-flash", history=history)

    def _load_and_format_history(self, limit: int = None):

        raw_history = load_history(
            user_id=self.user_id, conversation_id=self.conversation_id, limit=limit
        )

        formatted_history = []
        for content, role in raw_history:
            formatted_history.append(Content(role=role, parts=[Part(text=content)]))

        return formatted_history

    def ask(self, message: str) -> str:
        response = self.chat.send_message(message)
        ai_message = response.text
        recent_history = self.chat.get_history()[-2:]

        for content in recent_history:
            save_message(
                conversation_id=self.conversation_id,
                role=content.role,
                content=content.parts[0].text,
            )

        return ai_message

    def reload_history(self, limit: int = None):
        history = self._load_and_format_history(limit)
        self.chat = self.client.chats.create(model="gemini-2.5-flash", history=history)


class Application:
    def __init__(self):
        self.commands = {
            0: self.show_menu,
            1: self.register,
            2: self.login,
            3: sys.exit,
        }
        self.menu = """
╔════════════════════════════════════╗
║        AI CHATBOT - MENU           ║
╠════════════════════════════════════╣
║  0. Show Menu                      ║
║  1. Register                       ║
║  2. Login                          ║
║  3. Exit                           ║
╚════════════════════════════════════╝
"""

    def show_menu(self):
        print(self.menu)

    def register(self, username: str = None):
        if username:
            print(f"Username: {username}")
        else:
            username = input("Username: ").strip()

        password1 = getpass("Password: ")
        password2 = getpass("Password (again): ")

        if password1 != password2:
            print("❌ Passwords do not match. Please try again.\n")
            self.register(username=username)
            return

        try:
            user = register_user(username=username, password=password1)
            print(f"✅ Registered successfully! Welcome, {username}!\n")
        except DuplicateUser as e:
            print(f"❌ {e}\n")
        except Exception as e:
            print(f"❌ Registration failed: {e}\n")

    def login(self):
        print("\n--- LOGIN ---")

        username = input("Username: ").strip()
        password = getpass("Password: ")

        try:
            user_id = login_user(username=username, password=password)
            print(f"✅ Welcome back, {username}!\n")

            self.chat_session(user_id, username)

        except UserNotFound as e:
            print(f"❌ {e}\n")
        except Exception as e:
            print(f"❌ Login failed: {e}\n")

    def chat_session(self, user_id: int, username: str):
        print("Commands:")
        print("  /bye     - Exit chat")
        print("  /new     - Start new conversation")
        print("  /list    - List all conversations")
        print("  /help    - Show this help")

        agent = Agent(user_id=user_id)

        while True:
            try:
                user_message = input(f"{username}: ").strip()

                if not user_message:
                    continue

                if user_message.lower() == "/bye":
                    print("\n👋 Goodbye!\n")
                    break

                elif user_message.lower() == "/new":
                    conversation_id = create_conversation(user_id, title="New Chat")
                    agent = Agent(user_id=user_id, conversation_id=conversation_id)
                    print("✅ Started new conversation!\n")
                    continue
                elif user_message.lower() == "/debug":
                    print(f"\nDEBUG INFO:")
                    print(f"Your user_id: {user_id}")
                    print(f"Current conversation_id: {agent.conversation_id}")
                    conversations = get_user_conversations(user_id)
                    print(f"Your conversations: {conversations}\n")
                    continue
                elif user_message.lower() == "/list":
                    conversations = get_user_conversations(user_id)

                    if not conversations:
                        print("❌ No conversations found.\n")
                        continue

                    print("\n--- Your Conversations ---")
                    for conv in conversations:
                        current = (
                            "  ← (current)"
                            if conv["id"] == agent.conversation_id
                            else ""
                        )
                        print(
                            f"  ID: {conv['id']} | {conv['title']} | {conv['updated_at']}{current}"
                        )

                    switch_input = input(
                        "\nSwitch to conversation? Enter ID or press Enter to cancel: "
                    ).strip()

                    if not switch_input:
                        print()
                        continue

                    try:
                        conv_id = int(switch_input)

                        if not any(c["id"] == conv_id for c in conversations):
                            print("❌ Conversation not found.\n")
                            continue

                        agent = Agent(user_id=user_id, conversation_id=conv_id)
                        print(f"✅ Switched to conversation #{conv_id}\n")

                    except ValueError:
                        print("❌ Invalid conversation ID.\n")

                    continue

                elif user_message.lower() == "/help":
                    print("\nCommands:")
                    print("  /bye    - Exit chat")
                    print("  /new    - Start new conversation")
                    print("  /list   - List conversations (with option to switch)")
                    print("  /help   - Show this help\n")
                    continue

                ai_message = agent.ask(user_message)
                print(f"model: {ai_message}\n")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                break
            except Exception as e:
                print(f"❌ Error: {e}\n")

    def run(self):
        print("\n" + "=" * 50)
        print("  🤖 AI CHATBOT")
        print("=" * 50)

        self.show_menu()
        while True:
            try:
                command_input = input("\nCommand ID: ").strip()

                if not command_input:
                    continue

                try:
                    command_id = int(command_input)
                except ValueError:
                    print("❌ Please enter a valid number.")
                    continue

                if command_id not in self.commands:
                    print(
                        f"❌ Invalid command ID. Choose from: {list(self.commands.keys())}"
                    )
                    continue

                command = self.commands[command_id]
                command()

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"❌ Error: {e}")


if __name__ == "__main__":
    app = Application()
    app.run()
