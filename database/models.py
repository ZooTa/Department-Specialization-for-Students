from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from .base_models import GlobalBase, ProjectBase


# Global database models

class Faculty(GlobalBase):
    __tablename__ = 'faculty'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    departments = relationship('Department', back_populates='faculty', cascade='all, delete-orphan')


class Department(GlobalBase):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    student_capacity = Column(Integer, nullable=False)
    faculty_id = Column(Integer, ForeignKey('faculty.id'), nullable=False)

    faculty = relationship('Faculty', back_populates='departments')
    programs = relationship('Program', back_populates='department', cascade='all, delete-orphan')
    specializations = relationship('Specialization', back_populates='department', cascade='all, delete-orphan')

    # department_heads = relationship('DepartmentHead', back_populates='department')
    # assignment_results = relationship('AssignmentResult', back_populates='department')
    # preferences = relationship('Preferences', back_populates='department')


class Program(GlobalBase):
    __tablename__ = 'program'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)
    gpa_threshold = Column(Float, nullable=False)
    student_capacity = Column(Integer, nullable=False)



    department = relationship('Department', back_populates='programs')

    specializations = relationship('Specialization', back_populates='program', cascade='all, delete-orphan')
    subjects_required = relationship('RequiredSubject', back_populates='program', cascade='all, delete-orphan')

    # assignment_results = relationship('AssignmentResult', back_populates='program')
    # preferences = relationship('Preferences', back_populates='program')


class Specialization(GlobalBase):
    __tablename__ = 'specialization'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    gpa_threshold = Column(Float, nullable=False)
    student_capacity = Column(Integer, nullable=False)
    program_id = Column(Integer, ForeignKey('program.id'), nullable=False)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)

    department = relationship('Department', back_populates='specializations')
    program = relationship('Program', back_populates='specializations')

    subjects_required = relationship('RequiredSubject', back_populates='specialization', cascade='all, delete-orphan')

    # assignment_results = relationship('AssignmentResult', back_populates='specialization')
    # preferences = relationship('Preferences', back_populates='specialization')



class RequiredSubject (GlobalBase):
    __tablename__ = 'subjects_required'
    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    min_grade = Column(Integer, nullable=False)

    program = relationship('Program', back_populates='subjects_required')
    specialization = relationship('Specialization', back_populates='subjects_required')

class Person(GlobalBase):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    ssn = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

    admin = relationship('Admin', back_populates='person',
                         uselist=False,
                         cascade="all, delete-orphan",
                         single_parent=True)

    department_head = relationship('DepartmentHead', back_populates='person',
                                   uselist=False,
                                   cascade="all, delete-orphan",
                                   single_parent=True)


class DepartmentHead(GlobalBase):
    __tablename__ = 'department_head'

    person_id = Column(Integer, ForeignKey('person.id', ondelete="CASCADE"), primary_key=True)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)

    person = relationship('Person', back_populates='department_head',
                          cascade="all, delete",  # delete person if head is deleted
                          single_parent=True)

    department = relationship('Department', back_populates='department_heads')


class Admin(GlobalBase):
    __tablename__ = 'admin'

    person_id = Column(Integer, ForeignKey('person.id', ondelete="CASCADE"), primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    person = relationship('Person', back_populates='admin',
                          cascade="all, delete",  # delete person if admin is deleted
                          single_parent=True)

    projects = relationship('Project', back_populates='creator')
    action_logs = relationship('ActionLog', back_populates='admin')


# class ActionLog(GlobalBase):
#     __tablename__ = 'action_log'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('admin.person_id'), nullable=False)
#     action_name = Column(String, nullable=False)
#     action_details = Column(Text, nullable=False)
#     timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
#
#     admin = relationship('Admin', back_populates='action_logs')


class Project(GlobalBase):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    type = Column(String, nullable=False)  # 'department' or 'program' or 'specialization'
    excel_file_name = Column(String, nullable=False)
    directory = Column(String, nullable=False)  # path to project folder
    # created_by = Column(Integer, ForeignKey('admin.person_id'), nullable=False)
    # created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    creator = relationship('Admin', back_populates='projects')
    # action_logs = relationship('ActionLog', back_populates='admin')


# Project database models

class Student(ProjectBase):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    ssn = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    gpa = Column(Float, nullable=False)
    eligibility_rank = Column(Integer, nullable=False)
    passed_subjects = Column(Text, nullable=False)

    student_grades = relationship('StudentGrades', back_populates='student', cascade='all, delete-orphan')
    preferences = relationship('Preferences', back_populates='student', cascade='all, delete-orphan')
    assignment_results = relationship('StudentAssignment', back_populates='student', cascade='all, delete-orphan')


class StudentGrades(ProjectBase):
    __tablename__ = 'student_grades'
    id = Column(Integer,
                primary_key=True)  # Unique ID for each grade record عشان ممكن تسقط ف تعيد المادة ف الكود هيظهر مرتين
    subject_code = Column(String, nullable=False)
    semester = Column(String, nullable=False)
    points = Column(Float, nullable=False)
    credit_hours = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey('student.id'))

    student = relationship('Student', back_populates='student_grades')


class ProjectInfo(ProjectBase):
    __tablename__ = 'project_info'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    # created_at = Column(DateTime)
    # preference_count = Column(Integer, nullable=True)

    preferences = relationship('Preferences', back_populates='project', cascade='all, delete-orphan')
    preferences = relationship('Preferences', back_populates='project', cascade='all, delete-orphan')
    assignment_results = relationship('StudentAssignment', back_populates='project', cascade='all, delete-orphan')


class Preferences(ProjectBase):
    __tablename__ = 'preferences'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    student_id = Column(Integer, ForeignKey('student.id'))
    project_id = Column(Integer, ForeignKey('project_info.id'))
    preference_order = Column(Integer)

    # Only one of these will be used, based on project type
    department_id = Column(Integer, nullable=True)
    program_id = Column(Integer, nullable=True)
    specialization_id = Column(Integer, nullable=True)

    student = relationship('Student', back_populates='preferences')
    project = relationship('ProjectInfo', back_populates='preferences')


class StudentAssignment(ProjectBase):
    __tablename__ = 'assignment_result'

    __table_args__ = (
        UniqueConstraint('student_id', 'project_id', name='uix_student_project'),
    )

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project_info.id'), nullable=False) # Foreign key to project and if it not important delete
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)

    # One of these based on project type
    department_id = Column(Integer, nullable=True)
    program_id = Column(Integer, nullable=True)
    specialization_id = Column(Integer, nullable=True)

    assignment_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)  # e.g., "assigned", "pending", "failed"

    project = relationship('ProjectInfo', back_populates='assignment_results')
    student = relationship('Student', back_populates='assignment_results')

#
#
#
#
# class Notification(Base):
#     __tablename__ = 'notification'
#     id = Column(Integer, primary_key=True)
#     project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
#     recipient_email = Column(String, nullable=False)
#     message_type = Column(String, nullable=False)
#     status = Column(String, nullable=False)
#     sent_at = Column(DateTime, nullable=False)
#
#     project = relationship('Project', back_populates='notifications')
#


# class ActionLog(Base):
#     __tablename__ = 'action_log'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('admin.person_id'))
#     action_name = Column(String)
#     action_details = Column(Text)
#     timestamp = Column(DateTime, default=datetime.utcnow)
#
#     admin = relationship('Admin', back_populates='action_logs')

#
# General Imports and Base:
# # Primary Key
#
# # ID column: primary key, unique, integer
#
# # Attributes
#
# # Name column: string, not necessarily unique
#
# # Relationships
#
# # Relationship with Department: one faculty can have many departments
#
# Department:
# # Primary Key
#
# # ID column: primary key, unique, integer
#
# # Attributes
#
# # Name column: string, not necessarily unique
#
# # Student capacity: integer
#
# #Foreign keys
#
# # Foreign key to Faculty: non-nullable
#
# # Relationships
#
# # Relationship with Faculty: many departments to one faculty
#
# # Relationship with Program: one department can have many programs
#
# # Relationship with Specialization: one department can have many specializations
#
# Program:
# # Primary Key
#
# # ID column: primary key, unique, integer
#
# # Attributes
#
# # Name column: string, not necessarily unique
#
# # Criteria to join the program
#
# # Subjects required to join
#
# # GPA threshold for the program
#
# # Capacity of the program
#
# # Foreign Keys
#
# # Foreign key to Department: non-nullable
#
# # Relationships
#
# # Relationship with Department: many programs to one department
#
# # Relationship with Specialization: one program can have many specializations
#
# Specialization:
# # Primary Key
#
# # ID column: primary key, unique, integer
#
# # Attributes
#
# # Name column: string, not necessarily unique
#
# # Criteria to join the specialization
#
# # Subjects required to join
#
# # GPA threshold for the specialization
#
# # Capacity of the specialization
#
# # Foreign Keys
#
# # Foreign key to Program: non-nullable
#
# # Relationships
#
# # Relationship with Program: many specializations to one program
#
# Admin:
# # Primary Key
#
# # ID column: primary key, unique, integer
#
# # Attributes
#
# # Name column: string, not necessarily unique
#
# # SSN column: unique string
#
# # Email column: unique string
#
# # Phone number column: string
#
# # Username column: unique string
#
# # Password column: string
#
# # Role column: string, can be 'admin', 'super admin', or 'system admin'
#
# # Created by column: integer, references another admin
#
# # Created at column: datetime
#
# # Relationships
#
# # Relationship with ActionLog: one admin can have many action logs
#
# Department Head:
# # Primary Key
#
# # ID column: primary key, unique, integer
#
# # Attributes
#
# # Name column: string, not necessarily unique
#
# # Email column: unique string
#
# # Phone number column: string
#
# # Foreign Keys
#
# # Foreign key to Department: non-nullable
#
# # Relationships
#
# # Relationship with Department: one-to-one relationship
#
# Student:
# # Primary Key
#
# # ID column: primary key, unique, integer
#
# # Attributes
#
# # SSN column: unique string
#
# # Name column: string, not necessarily unique
#
# # Email column: unique string
#
# # Phone number column: string
#
# # Gender column: string
#
# # GPA column: float
#
# # Relationships
#
# # Relationship with Preferences: one student can have many preferences
#
# # Relationship with AssignmentResults: one student can have many assignment results
#
# # Relationship with StudentGrades: one student can have many grades
#
# Preferences:
# # Primary Key
#
# # Composite primary key: student_id, project_id, preference_order
#
# # Foreign Keys
#
# # Optional foreign keys for department, program, and specialization
#
# # Relationships
#
# # Relationship with Student: one preference belongs to one student
#
# # Relationship with Project: one preference belongs to one project
#
# Assignment Result:
# # Primary Key
#
# # ID column: primary key, unique, integer
#
# # Foreign Keys
#
# # Student ID: non-nullable
#
# # Optional foreign keys for department, program, and specialization
#
# # Relationships
#
# # Relationship with Student: one assignment result belongs to one student
#
# Student Grades:
# # Primary Key
#
# # ID column: primary key, unique, integer
#
# # Foreign Keys
#
# # Student ID: non-nullable
#
# # Attributes
#
# # Subject code: string
#
# # Semester: string
#
# # Credit hours: integer
#
# # Points: float
#
# # Relationships
#
# # Relationship with Student: one grade belongs to one student
#
# Project:
# # Primary Key
#
# # ID column: primary key, unique, integer
#
# # Attributes
#
# # Name column: string, not necessarily unique
#
# # Excel file name: string
#
# # Status column: string, indicates if the project is active, completed, etc.
#
# # Status column: string, indicates if the project is active, completed, etc.
#
# # Directory column: string, indicates if the project is department, program, specialization.
#
# # Created by column: integer, references an admin
#
# # Created at column: datetime
#
# # Relationships
#
# # Relationship with AssignmentResult: one project can have many assignment results
#
# # Relationship with Notification: one project can have many notifications
#
# Notification:
# # Primary Key
#
# # ID column: primary key, unique, integer
#
# # Attributes
#
# # Recipient email: string
#
# # Message type: string, indicates the type of recipient (e.g., admin, super admin)
#
# # Status: string, indicates if the notification has been sent
#
# # Sent at: datetime, indicates when the notification was sent
#
