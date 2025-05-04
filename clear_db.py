from app import app, db, User, Message, Global_Messages

def clear_database():
    with app.app_context():
        db.drop_all()
        
        db.create_all()
        
        print("Database has been cleared successfully!")

if __name__ == "__main__":
    clear_database() 