# services/faculty_service.py

from sqlalchemy.orm import Session
from database.models import Faculty

class FacultyService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name):
        new_faculty = Faculty(name=name)
        self.session.add(new_faculty)
        self.session.commit()
        return new_faculty

    def get(self, faculty_id):
        return self.session.query(Faculty).get(faculty_id)

    def update(self, faculty_id, name=None):
        faculty = self.get(faculty_id)
        if faculty:
            if name is not None:
                faculty.name = name
            self.session.commit()
        return faculty

    def delete(self, faculty_id):
        faculty = self.get(faculty_id)
        if faculty:
            self.session.delete(faculty)
            self.session.commit()
        return faculty

    def search(self, faculty_id=None, name=None):
        query = self.session.query(Faculty)
        if faculty_id is not None:
            query = query.filter(Faculty.id == faculty_id)
        if name is not None:
            query = query.filter(Faculty.name.ilike(f'%{name}%'))
        return query.all()
