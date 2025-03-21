# services/department_service.py

from sqlalchemy.orm import Session
from database.models import Department

class DepartmentService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name, faculty_id, student_capacity):
        new_department = Department(name=name, faculty_id=faculty_id, student_capacity=student_capacity)
        self.session.add(new_department)
        self.session.commit()
        return new_department

    def get(self, department_id):
        return self.session.query(Department).get(department_id)

    def update(self, department_id, name=None, faculty_id=None, student_capacity=None):
        department = self.get(department_id)
        if department:
            if name is not None:
                department.name = name
            if faculty_id is not None:
                department.faculty_id = faculty_id
            if student_capacity is not None:
                department.student_capacity = student_capacity
            self.session.commit()
        return department

    def delete(self, department_id):
        department = self.get(department_id)
        if department:
            self.session.delete(department)
            self.session.commit()
        return department

    def search(self, department_id=None, name=None):
        query = self.session.query(Department)
        if department_id is not None:
            query = query.filter(Department.id == department_id)
        if name is not None:
            query = query.filter(Department.name.ilike(f'%{name}%'))
        return query.all()
