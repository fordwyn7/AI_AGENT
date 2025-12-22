from database import db_manager, User, Conversation, Message, UserPreference

def test_database():
    print("🧪 Testing AI Chatbot Database")
    print()
    with db_manager.session_scope() as session:
        print("1️⃣  Creating test user...")
        user = User(
            username='test_user',
            full_name='Test User'
        )
        session.add(user)
        session.flush()
        print(f"   ✅ User created with ID: {user.id}")
        print()
        print("2️⃣  Creating user preferences...")
        preferences = UserPreference(
            user_id=user.id,
            ai_model='gpt-3.5-turbo',
        )
        session.add(preferences)
        print("   ✅ Preferences created")
        
        print("3️⃣  Creating conversation...")
        conversation = Conversation(
            user_id=user.id,
            title='Test Conversation'
        )
        session.add(conversation)
        session.flush()
        print(f"   ✅ Conversation created with ID: {conversation.id}")
        
        print("4️⃣  Creating messages...")
        message1 = Message(
            conversation_id=conversation.id,
            role='user',
            content='Hello, AI!'
        )
        message2 = Message(
            conversation_id=conversation.id,
            role='model',
            content='*random text from AI'
        )
        session.add_all([message1, message2])
        print("   ✅ Messages created")
        
        session.commit()
        
        print()
        print("5️⃣  Querying data...")
        
        test_user = session.query(User).filter_by(username='test_user').first()
        print(f"   📊 User: {test_user.username}")
        print(f"   📊 Preferences: AI Model = {test_user.preferences.ai_model}")
        print(f"   📊 Conversations: {len(test_user.conversations)}")
        print(f"   📊 Messages in first conversation: {len(test_user.conversations[0].messages)}")
        
        for msg in test_user.conversations[0].messages:
            print(f"      💬 {msg.role}: {msg.content}")
        
        print()
        print("✅ All tests passed! Database is working perfectly!")
        print()
        
        response = input("🗑️  Delete test data? (y/n): ")
        if response.lower() in ['y', 'yes']:
            session.delete(user)
            session.commit()
            print("   ✅ Test data cleaned up")

if __name__ == '__main__':
    test_database()