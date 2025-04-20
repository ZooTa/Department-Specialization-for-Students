# services/specialization_service.py

from sqlalchemy.orm import Session

from database.models import Specialization


class SpecializationService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name, subjects_required, gpa_threshold, student_capacity, program_id, department_id):
        new_specialization = Specialization(
            name=name,
            subjects_required=subjects_required,
            gpa_threshold=gpa_threshold,
            student_capacity=student_capacity,
            program_id=program_id,
            department_id=department_id
        )
        self.session.add(new_specialization)
        self.session.commit()
        return new_specialization

    def get(self, specialization_id):
        return self.session.get(Specialization,
                                specialization_id)  # or self.session.query(Specialization).get(specialization_id)

    def get_all(self):
        return self.session.query(Specialization).all()

    def update(self, specialization_id, name=None, subjects_required=None, gpa_threshold=None, student_capacity=None,
               program_id=None, department_id=None):
        specialization = self.get(specialization_id)
        if not specialization:
            print("Specialization not found.")
            return None

        updated = False

        if name is not None:
            specialization.name = name
            updated = True
        if subjects_required is not None:
            specialization.subjects_required = subjects_required
            updated = True
        if gpa_threshold is not None:
            specialization.gpa_threshold = gpa_threshold
            updated = True
        if student_capacity is not None:
            specialization.student_capacity = student_capacity
            updated = True
        if program_id is not None:
            specialization.program_id = program_id
            updated = True
        if department_id is not None:
            specialization.department_id = department_id
            updated = True

        if updated:
            self.session.commit()
            print("Specialization updated successfully.")
        else:
            print("Nothing to update.")

        return specialization

    def delete(self, specialization_id):
        specialization = self.get(specialization_id)
        if not specialization:
            print("Specialization not found.")
            return

        self.session.delete(specialization)
        self.session.commit()
        return specialization
