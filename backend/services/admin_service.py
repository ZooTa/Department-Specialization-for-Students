# services/admin_service.py

from sqlalchemy.orm import Session

from ..database.models import Admin


class AdminService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name, username, password, role):
        # Create a new Admin linked to the Person
        new_admin = Admin(
            name=name,
            username=username,
            role=role
            # created_at=datetime.utcnow()
        )
        new_admin.set_password(password)
        self.session.add(new_admin)
        self.session.commit()
        return new_admin

    def get(self, admin_id):
        return self.session.get(Admin, admin_id)

    def get_all(self):
        return self.session.query(Admin).all()

    def update(self, admin_id, name=None, ssn=None, email=None, phone_number=None, username=None,
               password=None, role=None):
        admin = self.get(admin_id)
        if not admin:
            print("Admin not found.")
            return None

        updated = False

        # Update Admin details
        if name is not None:
            admin.name = name
            updated = True
        if username is not None:
            admin.username = username
            updated = True
        if password is not None:
            admin.set_password(password)
            updated = True
        if role is not None:
            admin.role = role
            updated = True

        if updated:
            self.session.commit()
            print("Admin updated successfully.")
        else:
            print("Nothing to update.")

        return admin

    def delete(self, admin_id):
        admin = self.get(admin_id)
        if not admin:
            print("Admin not found.")
            return

        # Deleting the admin will also delete the associated person due to cascade settings
        self.session.delete(admin)
        self.session.commit()
        return admin

    def login(self, username, password):
        admin = self.session.query(Admin).filter_by(username=username).first()
        if admin and admin.check_password(password):
            print("Login successful.")
            return admin.role
        print("Invalid username or password.")
        return None

    def get_by_username(self, username: str):
        return self.session.query(Admin).filter(Admin.username == username).first()
