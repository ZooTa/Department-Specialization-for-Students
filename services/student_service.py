# services/student_service.py

from sqlalchemy.orm import Session
from database.models import Student

class StudentService:
    def __init__(self, session: Session, current_user):
        self.session = session
        self.current_user = current_user

    def update(self, student_id, **kwargs):
        if not self.is_authorized('update'):
            raise PermissionError("You do not have permission to update student data.")

        student = self.get(student_id)
        if student:
            for key, value in kwargs.items():
                setattr(student, key, value)
            self.session.commit()
        return student

    def delete(self, student_id):
        if not self.is_authorized('delete'):
            raise PermissionError("You do not have permission to delete student data.")

        student = self.get(student_id)
        if student:
            self.session.delete(student)
            self.session.commit()
        return student

    def search(self, student_id=None, name=None):
        query = self.session.query(Student)
        if student_id is not None:
            query = query.filter(Student.id == student_id)
        if name is not None:
            query = query.filter(Student.name.ilike(f'%{name}%'))
        return query.all()

    def is_authorized(self, action):
        return self.current_user.role == 'system admin'

    def get(self, student_id):
        return self.session.query(Student).get(student_id)

