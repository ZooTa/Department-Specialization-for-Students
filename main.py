from backend.services.admin_service import AdminService
from backend.database.database_config import get_session, init_user_db, init_project_db



# Initialize the database

init_user_db()
init_project_db("Class 2025")

# Create a session
with get_session() as session:
    # Example usage of the session
    admin_service = AdminService(session)

    # Add a new admin
    # admin_service.create("Ahmed Hussein", "ramen_goblin", "123", "admin")

    # # Method to set password (hashing)
    # admin_service.login("ramen_goblin", "123")
    # print("hi hi \n")
    # admin_service.login("ramen_goblin", "000")
