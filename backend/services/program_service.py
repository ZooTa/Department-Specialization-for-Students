# services/program_service.py

from sqlalchemy.orm import Session

from ..database.models import Program


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
        return self.session.get(Program, program_id)  # or self.session.query(Program).get(program_id)

    def get_all(self):
        return self.session.query(Program).all()

    def update(self, program_id, name=None, department_id=None, subjects_required=None, gpa_threshold=None,
               student_capacity=None):
        program = self.get(program_id)
        if not program:
            print("Program not found.")
            return None

        updated = False

        if name is not None:
            program.name = name
            updated = True
        if department_id is not None:
            program.department_id = department_id
            updated = True
        if subjects_required is not None:
            program.subjects_required = subjects_required
            updated = True
        if gpa_threshold is not None:
            program.gpa_threshold = gpa_threshold
            updated = True
        if student_capacity is not None:
            program.student_capacity = student_capacity
            updated = True

        if updated:
            self.session.commit()
            print("Program updated successfully.")
        else:
            print("Nothing to update.")

        return program

    def delete(self, program_id):
        program = self.get(program_id)
        if not program:
            print("Program not found.")
            return

        self.session.delete(program)
        self.session.commit()
        return program
