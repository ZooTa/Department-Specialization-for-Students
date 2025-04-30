# services/student_service.py

from sqlalchemy.orm import Session

from ..database.models import Student


class StudentService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, id, name, ssn, email, phone_number, gender, gpa, eligibility_rank, passed_subjects):
        # Create a new Student linked to the Person
        new_student = Student(
            id=id,
            name=name,
            email=email,
            gpa=gpa
            # ssn=ssn,
            # phone_number=phone_number,
            # gender=gender,
            # eligibility_rank=eligibility_rank,
            # passed_subjects=passed_subjects
        )
        self.session.add(new_student)
        self.session.commit()
        return new_student

    def get(self, student_id):
        return self.session.get(Student, student_id)

    def get_all(self):
        return self.session.query(Student).all()

    def update(self, student_id, id_num=None, name=None, email=None, gpa=None):
        student = self.get(student_id)
        if not student:
            print("Student not found.")
            return None

        updated = False

        # Update Student details
        if id_num is not None:
            student.id_num = id_num
            updated = True
        if name is not None:
            student.name = name
            updated = True
        if email is not None:
            student.email = email
            updated = True
        if gpa is not None:
            student.gpa = gpa
            updated = True

        if updated:
            self.session.commit()
            print("Student updated successfully.")
        else:
            print("Nothing to update.")

        return student

    def delete(self, student_id):
        student = self.get(student_id)
        if not student:
            print("Student not found.")
            return

        # Deleting the student will also delete the associated person due to cascade settings
        self.session.delete(student)
        self.session.commit()
        return student

    def get_mean_gpa(self):
        students = self.get_all()
        if not students:
            return 0.00
        total_gpa = sum(student.gpa for student in students)
        mean_gpa = total_gpa / len(students)
        return mean_gpa
