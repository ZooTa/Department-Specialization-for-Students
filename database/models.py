from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from base_models import Base


class Faculty(Base):
    __tablename__ = 'faculty'

    # Primary Key
    # ID column: primary key, unique, integer
    id = Column(Integer, primary_key=True, unique=True)

    # Attributes
    # Name column: string, not necessarily unique
    name = Column(String, nullable=False)

    # Relationships
    # Relationship with Department: one faculty can have many departments
    departments = relationship('Department', back_populates='faculty')



class Department(Base):
    __tablename__ = 'department'

    # Primary Key
    # ID column: primary key, unique, integer
    id = Column(Integer, primary_key=True, unique=True)

    # Attributes
    # Name column: string, not necessarily unique
    name = Column(String, nullable=False)
    # Student capacity: integer
    student_capacity = Column(Integer, nullable=False)

    #Foreign keys
    # Foreign key to Faculty: non-nullable
    faculty_id = Column(Integer, ForeignKey('faculty.id'), nullable=False)

    # Relationships
    # Relationship with Faculty: many departments to one faculty
    faculty = relationship('Faculty', back_populates='departments')
    # Relationship with Program: one department can have many programs
    programs = relationship('Program', back_populates='department')
    # Relationship with Specialization: one department can have many specializations
    specializations = relationship('Specialization', back_populates='department')



class Program(Base):
    __tablename__ = 'program'

    # Primary Key
    # ID column: primary key, unique, integer
    id = Column(Integer, primary_key=True, unique=True)

    # Attributes
    # Name column: string, not necessarily unique
    name = Column(String, nullable=False)
    # Criteria to join the program
    subjects_required = Column(String, nullable=False)  # Subjects required to join
    gpa_threshold = Column(Float, nullable=False)       # GPA threshold for the program
    student_capacity = Column(Integer, nullable=False)  # Capacity of the program

    # Foreign Keys
    # Foreign key to Department: non-nullable
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)

    # Relationships
    # Relationship with Department: many programs to one department
    department = relationship('Department', back_populates='programs')
    # Relationship with Specialization: one program can have many specializations
    specializations = relationship('Specialization', back_populates='program')



class Specialization(Base):
    __tablename__ = 'specialization'

    # Primary Key
    # ID column: primary key, unique, integer
    id = Column(Integer, primary_key=True, unique=True)

    # Attributes
    # Name column: string, not necessarily unique
    name = Column(String, nullable=False)
    # Criteria to join the specialization
    subjects_required = Column(String, nullable=False)  # Subjects required to join
    gpa_threshold = Column(Float, nullable=False)       # GPA threshold for the specialization
    student_capacity = Column(Integer, nullable=False)  # Capacity of the specialization

    # Foreign Keys
    # Foreign key to Program: non-nullable
    program_id = Column(Integer, ForeignKey('program.id'), nullable=False)

    # Relationships
    # Relationship with Program: many specializations to one program
    program = relationship('Program', back_populates='specializations')



class Admin(Base):
    __tablename__ = 'admin'

    # Primary Key
    # ID column: primary key, unique, integer
    id = Column(Integer, primary_key=True, unique=True)

    # Attributes
    # Name column: string, not necessarily unique
    name = Column(String, nullable=False)
    # SSN column: unique string
    ssn = Column(String, unique=True, nullable=False)
    # Email column: unique string
    email = Column(String, unique=True, nullable=False)
    # Phone number column: string
    phone_number = Column(String, nullable=False)
    # Username column: unique string
    username = Column(String, unique=True, nullable=False)
    # Password column: string
    password = Column(String, nullable=False)
    # Role column: string, can be 'admin', 'super admin', or 'system admin'
    role = Column(String, nullable=False)
    # Created by column: integer, references another admin
    created_by = Column(Integer, ForeignKey('admin.id'), nullable=True)
    # Created at column: datetime
    created_at = Column(DateTime, nullable=False)

    # Relationships
    # Relationship with ActionLog: one admin can have many action logs
    action_logs = relationship('ActionLog', back_populates='admin')



class DepartmentHead(Base):
    __tablename__ = 'department_head'

    # Primary Key
    # ID column: primary key, unique, integer
    id = Column(Integer, primary_key=True, unique=True)

    # Attributes
    # Name column: string, not necessarily unique
    name = Column(String, nullable=False)
    # Email column: unique string
    email = Column(String, unique=True, nullable=False)
    # Phone number column: string
    phone_number = Column(String, nullable=False)

    # Foreign Keys
    # Foreign key to Department: non-nullable
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)

    # Relationships
    # Relationship with Department: one-to-one relationship
    department = relationship('Department', back_populates='department_head', uselist=False)



class Student(Base):
    __tablename__ = 'student'

    # Primary Key
    # ID column: primary key, unique, integer
    id = Column(Integer, primary_key=True, unique=True)  # ID given by the college

    # Attributes
    # SSN column: unique string
    ssn = Column(String, unique=True, nullable=False)
    # Name column: string, not necessarily unique
    name = Column(String, nullable=False)
    # Email column: unique string
    email = Column(String, unique=True, nullable=False)
    # Phone number column: string
    phone_number = Column(String, nullable=False)
    # Gender column: string
    gender = Column(String, nullable=False)
    # GPA column: float
    gpa = Column(Float, nullable=False)

    # Relationships
    # Relationship with Preferences: one student can have many preferences
    preferences = relationship('Preferences', back_populates='student')
    # Relationship with AssignmentResults: one student can have many assignment results
    assignment_results = relationship('AssignmentResult', back_populates='student')
    # Relationship with StudentGrades: one student can have many grades
    grades = relationship('StudentGrades', back_populates='student')



class Preferences(Base):
    __tablename__ = 'preferences'

    # Primary Key
    # Composite primary key: student_id, project_id, preference_order
    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'), primary_key=True)
    preference_order = Column(Integer, primary_key=True)

    preference = Column(String)

#     # Foreign Keys
#     # Optional foreign keys for department, program, and specialization
#     department_id = Column(Integer, ForeignKey('department.id'), nullable=True)
#     program_id = Column(Integer, ForeignKey('program.id'), nullable=True)
#     specialization_id = Column(Integer, ForeignKey('specialization.id'), nullable=True)

    # Relationships
    # Relationship with Student: one preference belongs to one student
    student = relationship('Student', back_populates='preferences')
    # Relationship with Project: one preference belongs to one project
    project = relationship('Project', back_populates='preferences')



class AssignmentResult(Base):
    __tablename__ = 'assignment_result'

    # Primary Key
    # ID column: primary key, unique, integer
    id = Column(Integer, primary_key=True, unique=True)

    # Foreign Keys
    # Student ID: non-nullable
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    # Optional foreign keys for department, program, and specialization
    department_id = Column(Integer, ForeignKey('department.id'), nullable=True)
    program_id = Column(Integer, ForeignKey('program.id'), nullable=True)
    specialization_id = Column(Integer, ForeignKey('specialization.id'), nullable=True)

    # Relationships
    # Relationship with Student: one assignment result belongs to one student
    student = relationship('Student', back_populates='assignment_results')



class StudentGrades(Base):
    __tablename__ = 'student_grades'

    # Primary Key
    # ID column: primary key, unique, integer
    id = Column(Integer, primary_key=True, unique=True)

    # Foreign Keys
    # Student ID: non-nullable
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)

    # Attributes
    # Subject code: string
    subject_code = Column(String, nullable=False)
    # Semester: string
    semester = Column(String, nullable=False)
    # Credit hours: integer
    credit_hours = Column(Integer, nullable=False)
    # Points: float
    points = Column(Float, nullable=False)

    # Relationships
    # Relationship with Student: one grade belongs to one student
    student = relationship('Student', back_populates='grades')



class Project(Base):
    __tablename__ = 'project'

    # Primary Key
    # ID column: primary key, unique, integer
    id = Column(Integer, primary_key=True, unique=True)

    # Attributes
    # Name column: string, not necessarily unique
    name = Column(String, nullable=False)
    # Excel file name: string
    excel_file_name = Column(String, nullable=False)
    # Status column: string, indicates if the project is active, completed, etc.
    status = Column(String, nullable=False)
    # Status column: string, indicates if the project is active, completed, etc.
    type = Column(String, nullable=False)
    # Directory column: string, indicates if the project is department, program, specialization.
    directory = Column(String, nullable=False)
    # Created by column: integer, references an admin
    created_by = Column(Integer, ForeignKey('admin.id'), nullable=False)
    # Created at column: datetime
    created_at = Column(DateTime, nullable=False)

    # Relationships
    # Relationship with AssignmentResult: one project can have many assignment results
    assignment_results = relationship('AssignmentResult', back_populates='project')
    # Relationship with Notification: one project can have many notifications
    notifications = relationship('Notification', back_populates='project')



class Notification(Base):
    __tablename__ = 'notification'

    # Primary Key
    # ID column: primary key, unique, integer
    id = Column(Integer, primary_key=True, unique=True)

    # Attributes
    # Recipient email: string
    recipient_email = Column(String, nullable=False)
    # Message type: string, indicates the type of recipient (e.g., admin, super admin)
    message_type = Column(String, nullable=False)
    # Status: string, indicates if the notification has been sent
    status = Column(String, nullable=False)
    # Sent at: datetime, indicates when the notification was sent
    sent_at = Column(DateTime, nullable=True)

    # Foreign Keys
    # Project ID: non-nullable
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)

    # Relationships
    # Relationship with Project: one notification belongs to one project
    project = relationship('Project', back_populates='notifications')



class ActionLog(Base):
    __tablename__ = 'action_log'

    # Primary Key
    # ID column: primary key, unique, integer
    id = Column(Integer, primary_key=True, unique=True)

    # Attributes
    # Timestamp: datetime, indicates when the action was performed
    timestamp = Column(DateTime, nullable=False)
    # Action name: string, describes the action performed
    action_name = Column(String, nullable=False)
    # Action details: string, provides additional details about the action
    action_details = Column(String, nullable=True)

    # Foreign Keys
    # User ID: non-nullable, links to the Admin table
    user_id = Column(Integer, ForeignKey('admin.id'), nullable=False)

    # Relationships
    # Relationship with Admin: one action log belongs to one admin
    admin = relationship('Admin', back_populates='action_logs')



