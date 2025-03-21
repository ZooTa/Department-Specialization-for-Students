# process/assignment_process.py

from services.student_service import StudentService
from services.program_service import ProgramService
from services.specialization_service import SpecializationService
from services.preferences_service import PreferencesService

class AssignmentProcess:
    def __init__(self, student_service, program_service, specialization_service, preferences_service):
        self.student_service = student_service
        self.program_service = program_service
        self.specialization_service = specialization_service
        self.preferences_service = preferences_service

    def assign_students(self, project_type):
        students = self.student_service.get_all_students()
        for student in students:
            preferences = self.preferences_service.get_preferences_for_student(student.id)
            if project_type == 'program':
                self.assign_to_program(student, preferences)
            elif project_type == 'specialization':
                self.assign_to_specialization(student, preferences)
            # Add logic for department if needed

    def assign_to_program(self, student, preferences):
        programs = self.program_service.get_all_programs()
        for preference in preferences:
            for program in programs:
                if program.id == preference.program_id and self.is_eligible_for_program(student, program):
                    self.student_service.assign_to_program(student.id, program.id)
                    return

    def assign_to_specialization(self, student, preferences):
        specializations = self.specialization_service.get_all_specializations()
        for preference in preferences:
            for specialization in specializations:
                if specialization.id == preference.specialization_id and self.is_eligible_for_specialization(student, specialization):
                    self.student_service.assign_to_specialization(student.id, specialization.id)
                    return

    def is_eligible_for_program(self, student, program):
        return (student.gpa >= program.gpa_threshold and
                self.has_completed_required_subjects(student, program.subjects_required) and
                self.is_within_capacity(student, program.student_capacity))

    def is_eligible_for_specialization(self, student, specialization):
        return (student.gpa >= specialization.gpa_threshold and
                self.has_completed_required_subjects(student, specialization.subjects_required) and
                self.is_within_capacity(student, specialization.student_capacity))

    def has_completed_required_subjects(self, student, required_subjects):
        return all(subject in student.passed_subjects for subject in required_subjects.split(','))

    def is_within_capacity(self, student, capacity):
        return student.eligibility_rank <= capacity
