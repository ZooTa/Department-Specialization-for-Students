# services/student_service.py

from sqlalchemy.orm import Session
from database.models import Student, Person

class StudentService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, first_name, last_name, ssn, email, phone_number, gender, gpa, eligibility_rank, passed_subjects):
        # Create a new Person
        new_person = Person(
            first_name=first_name,
            last_name=last_name,
            ssn=ssn,
            email=email,
            phone_number=phone_number
        )
        self.session.add(new_person)
        self.session.flush()  # Flush to get the new_person.id

        # Create a new Student linked to the Person
        new_student = Student(
            person_id=new_person.id,
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

        # Update Person details
        if first_name is not None:
            student.person.first_name = first_name
            updated = True
        if last_name is not None:
            student.person.last_name = last_name
            updated = True
        if ssn is not None:
            student.person.ssn = ssn
            updated = True
        if email is not None:
            student.person.email = email
            updated = True
        if phone_number is not None:
            student.person.phone_number = phone_number
            updated = True

        # Update Student details
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
