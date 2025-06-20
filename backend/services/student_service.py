# services/student_service.py

from sqlalchemy.orm import Session

from ..database.models import Student, Preferences, StudentAssignment

from sqlalchemy import desc

class StudentService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, id_num, name, email, gpa=0.0, preference_names=None):

        new_student = Student(
            id_num=id_num,
            name=name,
            email=email,
            gpa=gpa
        )

        # Add up to 6 preferences by name
        if preference_names:
            for i, name in enumerate(preference_names[:6], start=1):
                preference = Preferences(
                    name=name,
                    preference_order=i
                )
                new_student.preferences.append(preference)

        self.session.add(new_student)
        self.session.commit()
        return new_student

    def get(self, student_id):
        return self.session.get(Student, student_id)

    def get_all(self):
        return self.session.query(Student).all()

    def get_assigned_students(self, result_name):
        return (
            self.session.query(Student)
            .join(StudentAssignment, Student.assignment_results)
            .filter(StudentAssignment.result == result_name)
            .all()
        )

    def update(self, student_id, id_num=None, name=None, email=None, gpa=None, preference_names=None):
        student = self.get(student_id)
        if not student:
            print("Student not found.")
            return None

        updated = False

        # Update student fields
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

        # Update preferences if a new list is provided
        if preference_names:
            # Clear existing preferences
            student.preferences.clear()

            # Add the new ones
            for i, name in enumerate(preference_names[:6], start=1):
                new_pref = Preferences(
                    name=name,
                    preference_order=i
                )
                student.preferences.append(new_pref)

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


    def add_df(self, df):
        new_students= []
        for _, row in df.iterrows():
            new_student = Student(
                id_num=row["id"],
                name=row["name"],
                email=row["email"],
                gpa=row["gpa"],
            )
            new_students.append(new_student)
        self.session.add_all(new_students)
        self.session.commit()

    def ranked_students(self):
        return self.session.query(Student).order_by(desc(Student.gpa)).all()

    def assign_to_prefered_program(self, student_id, program_id, program_name):
        student = self.get(student_id)
        if not student:
            print("Student not found.")
            return None

        result = StudentAssignment(

            program_id=program_id,
            result=program_name
        )
        student.assignment_results.append(result)

        self.session.add(result)
        self.session.commit()
        return student

    def assign_to_prefered_specialization(self, student_id, specialization_id, specialization_name):
        student = self.get(student_id)
        if not student:
            print("Student not found.")
            return None

        result = StudentAssignment(
            specialization_id=specialization_id,
            result=specialization_name
        )
        student.assignment_results.append(result)

        self.session.add(result)
        self.session.commit()
        return student

    def assign_to_prefered_department(self, student_id, department_id, department_name):
        student = self.get(student_id)
        if not student:
            print("Student not found.")
            return None

        result = StudentAssignment(
            department_id=department_id,
            result=department_name
        )
        student.assignment_results.append(result)

        self.session.add(result)
        self.session.commit()
        return student

    def check_if_assigned(self, student_id: int) -> bool:
        """
        Check if a student has already been assigned to a project.
        Returns True if assigned, False otherwise.
        """
        return (
            self.session.query(StudentAssignment)
            .filter(StudentAssignment.student_id_num == student_id)
            .count() > 0
        )

    def check_if_any_assigned(self) -> bool:
        """
        Check if there are any assignments in the database.
        Returns True if assigned students exist, False otherwise.
        """
        return self.session.query(StudentAssignment).count() > 0

    def clear_all_assignments(self) -> None:
        """
        Delete all records from the StudentAssignment table.
        """
        self.session.query(StudentAssignment).delete()
        self.session.commit()
