import pandas as pd


class StudentDataProcessor:
    def __init__(self, student_file, form_file):
        self.student_file = student_file
        self.form_file = form_file
        self.df_grades = pd.read_csv(student_file)
        self.df_form = pd.read_csv(form_file)

    def create_student_table(self):
        # Extract emails from the form
        df_emails = self.df_form[['ID', 'Email']]

        # Filter to get only cumulative GPA rows
        df_gpa = self.df_grades.query('subject_code == "المعدل التراكمى"')
        df_gpa = df_gpa.drop(columns=['subject_code', 'cridet hours'])

        # Merge GPA data with emails
        df_student_table = pd.merge(df_gpa, df_emails, on='ID')

        return df_student_table

    def create_student_grade_table(self, student_table):
        # Filter out non-subject rows
        df_subjects = self.df_grades.query(
            'subject_code != "المعدل الفصلى" and subject_code != "المعدل التراكمى"'
        )
        df_subjects = df_subjects.drop(columns=['name'])

        # Keep only rows with IDs in student_table
        df_subjects = df_subjects[df_subjects['ID'].isin(student_table['ID'])]

        return df_subjects

    def create_student_preference_table(self):
        # Drop name and Email columns
        df_raw = self.df_form.drop(columns=['name', 'Email'])

        # Melt to long format
        df_melted = df_raw.melt(
            id_vars=['ID'],
            value_vars=['first prefrence', 'second prefrence', 'third prefrence'],
            var_name='preference_type',
            value_name='preference'
        )

        # Map preference order
        pref_map = {
            'first prefrence': 1,
            'second prefrence': 2,
            'third prefrence': 3
        }
        df_melted['preference_order'] = df_melted['preference_type'].map(pref_map)

        # Drop unneeded column and sort
        df_preference = df_melted.drop(columns=['preference_type'])
        df_preference = df_preference.sort_values(by=['ID', 'preference_order'])

        return df_preference

    def process_all_data(self):
        # Generate the student table, grade table, and preference table
        student_table = self.create_student_table()
        student_grades = self.create_student_grade_table(student_table)
        student_preferences = self.create_student_preference_table()

        return student_table, student_grades, student_preferences
