# process/assignment_process.py

seats_dict = {}


def can_exceed_capacity(student, name, student_service):
    assigned_students = student_service.get_assigned_students(name)
    if not assigned_students:
        return False

    lowest_gpa = min(s.gpa for s in assigned_students)

    return student.gpa == lowest_gpa


def pass_required_subjects(student, required_subjects):
    if not required_subjects:
        return True

    for subject in required_subjects:
        for studied_subject in student.student_grades:
            if subject.name.strip() == studied_subject.name.strip():
                if studied_subject.points < subject.min_grade:
                    return False
    return True


def is_within_capacity(student, name, student_service):
    global seats_dict
    if seats_dict[name] >= 1:
        return True
    elif can_exceed_capacity(student, name, student_service):
        return True
    else:
        return False


def is_eligible_for_program(student, program, student_service):
    return (student.gpa >= program.gpa_threshold and
            pass_required_subjects(student, program.subjects_required) and
            is_within_capacity(student, program.name.strip(), student_service))


def is_eligible_for_specialization(student, specialization, student_service):
    return (student.gpa >= specialization.gpa_threshold and
            pass_required_subjects(student, specialization.subjects_required) and
            is_within_capacity(student, specialization.name.strip(), student_service))


def is_eligible_for_department(student, department, student_service):
    return is_within_capacity(student, department.name.strip(), student_service)


class AssignmentProcess:

    def __init__(self, student_service, program_service, specialization_service, department_service, project_service):
        self.student_service = student_service
        self.program_service = program_service
        self.specialization_service = specialization_service
        self.department_service = department_service
        self.project_service = project_service

    def assign_students(self):
        project_type = self.project_service.get_project_type()
        students = self.student_service.ranked_students()
        self.set_seats_dict()

        # print("project_type:", project_type)
        #
        # print("Students ranked by GPA:")
        # for student in students:
        #     print(f"ID: {student.id_num}, Name: {student.name}, GPA: {student.gpa}")
        #
        # print("Seats available:")
        # for name, seats in seats_dict.items():
        #     print(f"{name}: {seats} seats")

        for student in students:
            preferences = student.preferences
            if project_type == 'program':
                # print(f"Assigning {student.name} to program based on preferences: {preferences}")
                self.assign_to_program(student, preferences)
            elif project_type == 'specialization':
                self.assign_to_specialization(student, preferences)
            elif project_type == 'department':
                self.assign_to_department(student, preferences)

    def clear_and_assign_students(self):
        if self.student_service.check_if_any_assigned():
            self.student_service.clear_all_assignments()
            self.set_seats_dict()

        self.assign_students()



    def assign_to_program(self, student, preferences):
        programs = self.program_service.get_all()
        for preference in preferences:
            for program in programs:
                # print(f"Checking preference: {preference.name.strip()} against program: {program.name.strip()}")
                if program.name.strip() == preference.name.strip():
                    print(f"Checking eligibility for {student.name} in {program.name}")
                    if is_eligible_for_program(student, program, self.student_service):
                        print(f"Assigning {student.name} to {program.name}")
                        self.student_service.assign_to_prefered_program(student.id_num, program.id,
                                                                        program.name.strip())
                        seats_dict[program.name.strip()] -= 1
                        return

    def assign_to_specialization(self, student, preferences):
        specializations = self.specialization_service.get_all_specializations()
        for preference in preferences:
            for specialization in specializations:
                if specialization.name.strip() == preference.name.strip():
                    print(f"Checking eligibility for {student.name} in {specialization.name}")
                    if is_eligible_for_specialization(student, specialization, self.student_service):
                        print(f"Assigning {student.name} to {specialization.name}")
                        self.student_service.assign_to_prefered_specialization(student.id_num, specialization.id,
                                                                               specialization.name.strip())
                        seats_dict[specialization.name.strip()] -= 1
                        return

    def assign_to_department(self, student, preferences):
        departments = self.department_service.get_all_departments()
        for preference in preferences:
            for department in departments:
                if department.name.strip() == preference.name.strip():
                    print(f"Checking eligibility for {student.name} in {department.name}")
                    if is_eligible_for_department(student, department, self.student_service):
                        print(f"Assigning {student.name} to {department.name}")
                        self.student_service.assign_to_prefered_department(student.id, department.id)
                        seats_dict[department.name.strip()] -= 1  # 🔻 Decrease available seat
                        return

    # def assign_to_specialization(self, student, preferences):
    #     specializations = self.specialization_service.get_all_specializations()
    #     for preference in preferences:
    #         for specialization in specializations:
    #             if specialization.name.strip() == preference.specialization_id and self.is_eligible_for_specialization(student, specialization):
    #                 self.student_service.assign_to_specialization(student.id, specialization.id)
    #                 return

    # def assign_to_department(self, student, preferences):
    #     departments = self.department_service.get_all_departments()
    #     for preference in preferences:
    #         for department in departments:
    #             if department.name.strip() == preference.name.strip() and self.is_eligible_for_department(department):
    #                 self.student_service.assign_to_department(student.id, department.id)
    #                 return

    #

    def set_seats_dict(self):
        global seats_dict

        project_type = self.project_service.get_project_type()
        if project_type == 'program':
            programs = self.program_service.get_all()
            for program in programs:
                seats_dict[program.name.strip()] = program.student_capacity
        elif project_type == 'specialization':
            specializations = self.specialization_service.get_all()
            for specialization in specializations:
                seats_dict[specialization.name.strip()] = specialization.student_capacity
        elif project_type == 'department':
            departments = self.department_service.get_all()
            for department in departments:
                seats_dict[department.name.strip()] = department.student_capacity
