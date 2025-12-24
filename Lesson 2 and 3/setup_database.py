from database import db_manager, config

def main():
    if not db_manager.test_connection():
        print("❌ Setup failed.")
        return
    
    print()
    response = input("📦 Create database tables? (y/n): ")
    if response.lower() in ['y', 'yes']:
        db_manager.create_tables()
        print("✅ Database setup complete!")
        print()
        print("Next steps:")
        print("  1. Run test_database.py to verify setup")
        print("  2. Start building your chatbot!")
    else:
        print("Setup cancelled.")


if __name__ == '__main__':
    main()