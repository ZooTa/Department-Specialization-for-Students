# services/program_service.py

from sqlalchemy.orm import Session
from database.models import Program

class ProgramService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name, department_id, subjects_required, gpa_threshold, student_capacity):
        new_program = Program(
            name=name,
            department_id=department_id,
            subjects_required=subjects_required,
            gpa_threshold=gpa_threshold,
            student_capacity=student_capacity
        )
        self.session.add(new_program)
        self.session.commit()
        return new_program

    def get(self, program_id):
        return self.session.query(Program).get(program_id)

    def update(self, program_id, name=None, department_id=None, subjects_required=None, gpa_threshold=None, student_capacity=None):
        program = self.get(program_id)
        if program:
            if name is not None:
                program.name = name
            if department_id is not None:
                program.department_id = department_id
            if subjects_required is not None:
                program.subjects_required = subjects_required
            if gpa_threshold is not None:
                program.gpa_threshold = gpa_threshold
            if student_capacity is not None:
                program.student_capacity = student_capacity
            self.session.commit()
        return program

    def delete(self, program_id):
        program = self.get(program_id)
        if program:
            self.session.delete(program)
            self.session.commit()
        return program

    def search(self, program_id=None, name=None):
        query = self.session.query(Program)
        if program_id is not None:
            query = query.filter(Program.id == program_id)
        if name is not None:
            query = query.filter(Program.name.ilike(f'%{name}%'))
        return query.all()
