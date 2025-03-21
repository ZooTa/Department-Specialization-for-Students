# services/specialization_service.py

from sqlalchemy.orm import Session
from database.models import Specialization

class SpecializationService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name, program_id, subjects_required, gpa_threshold, student_capacity):
        new_specialization = Specialization(
            name=name,
            program_id=program_id,
            subjects_required=subjects_required,
            gpa_threshold=gpa_threshold,
            student_capacity=student_capacity
        )
        self.session.add(new_specialization)
        self.session.commit()
        return new_specialization

    def get(self, specialization_id):
        return self.session.query(Specialization).get(specialization_id)

    def update(self, specialization_id, name=None, program_id=None, subjects_required=None, gpa_threshold=None, student_capacity=None):
        specialization = self.get(specialization_id)
        if specialization:
            if name is not None:
                specialization.name = name
            if program_id is not None:
                specialization.program_id = program_id
            if subjects_required is not None:
                specialization.subjects_required = subjects_required
            if gpa_threshold is not None:
                specialization.gpa_threshold = gpa_threshold
            if student_capacity is not None:
                specialization.student_capacity = student_capacity
            self.session.commit()
        return specialization

    def delete(self, specialization_id):
        specialization = self.get(specialization_id)
        if specialization:
            self.session.delete(specialization)
            self.session.commit()
        return specialization

    def search(self, specialization_id=None, name=None):
        query = self.session.query(Specialization)
        if specialization_id is not None:
            query = query.filter(Specialization.id == specialization_id)
        if name is not None:
            query = query.filter(Specialization.name.ilike(f'%{name}%'))
        return query.all()
