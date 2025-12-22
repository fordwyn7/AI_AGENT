from database import db_manager, config

def main():
    print(f"Environment: {config.ENVIRONMENT}")
    print(f"Database: {config.DB_NAME}")
    print(f"Host: {config.DB_HOST}:{config.DB_PORT}")
    print()
    print("🔍 Testing database connection...")
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