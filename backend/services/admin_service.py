# services/admin_service.py

from sqlalchemy.orm import Session
from database.models import Admin, Person
from datetime import datetime

class AdminService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, first_name, last_name, ssn, email, phone_number, username, password, role):
        # Create a new Person
        new_person = Person(
            first_name=first_name,
            last_name=last_name,
            ssn=ssn,
            email=email,
            phone_number=phone_number
        )
        self.session.add(new_person)
        self.session.flush()  # Flush to get the new_person.id

        # Create a new Admin linked to the Person
        new_admin = Admin(
            person_id=new_person.id,
            username=username,
            password=password,
            role=role,
            created_at=datetime.utcnow()
        )
        self.session.add(new_admin)
        self.session.commit()
        return new_admin

    def get(self, admin_id):
        return self.session.get(Admin, admin_id)

    def get_all(self):
        return self.session.query(Admin).all()

    def update(self, admin_id, first_name=None, last_name=None, ssn=None, email=None, phone_number=None, username=None, password=None, role=None):
        admin = self.get(admin_id)
        if not admin:
            print("Admin not found.")
            return None

        updated = False

        # Update Person details
        if first_name is not None:
            admin.person.first_name = first_name
            updated = True
        if last_name is not None:
            admin.person.last_name = last_name
            updated = True
        if ssn is not None:
            admin.person.ssn = ssn
            updated = True
        if email is not None:
            admin.person.email = email
            updated = True
        if phone_number is not None:
            admin.person.phone_number = phone_number
            updated = True

        # Update Admin details
        if username is not None:
            admin.username = username
            updated = True
        if password is not None:
            admin.password = password
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
