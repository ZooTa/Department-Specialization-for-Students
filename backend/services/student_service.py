# services/student_service.py

from sqlalchemy.orm import Session

from database.models import Student


class StudentService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, first_name, last_name, ssn, email, phone_number, gender, gpa, eligibility_rank, passed_subjects):
        # Create a new Student linked to the Person
        new_student = Student(
            first_name=first_name,
            last_name=last_name,
            ssn=ssn,
            email=email,
            phone_number=phone_number,
            gender=gender,
            gpa=gpa,
            eligibility_rank=eligibility_rank,
            passed_subjects=passed_subjects
        )
        self.session.add(new_student)
        self.session.commit()
        return new_student

    def get(self, student_id):
        return self.session.get(Student, student_id)

    def get_all(self):
        return self.session.query(Student).all()

    def update(self, student_id, first_name=None, last_name=None, ssn=None, email=None, phone_number=None, gender=None, gpa=None, eligibility_rank=None, passed_subjects=None):
        student = self.get(student_id)
        if not student:
            print("Student not found.")
            return None

        updated = False

        # Update Student details
        if first_name is not None:
            student.first_name = first_name
            updated = True
        if last_name is not None:
            student.last_name = last_name
            updated = True
        if ssn is not None:
            student.ssn = ssn
            updated = True
        if email is not None:
            student.email = email
            updated = True
        if phone_number is not None:
            student.phone_number = phone_number
            updated = True
        if gender is not None:
            student.gender = gender
            updated = True
        if gpa is not None:
            student.gpa = gpa
            updated = True
        if eligibility_rank is not None:
            student.eligibility_rank = eligibility_rank
            updated = True
        if passed_subjects is not None:
            student.passed_subjects = passed_subjects
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
        """
        Calculate the mean GPA of all students.
        """
        students = self.get_all()
        if not students:
            return 0.00

        total_gpa = sum(student.gpa for student in students)
        mean_gpa = total_gpa / len(students)
        return mean_gpa


