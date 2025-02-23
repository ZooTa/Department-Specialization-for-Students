---
icon: clipboard-list
---

# Use Cases

#### 1.1: Processing Student Preferences for Department Specialization

**Actors:**

* Administrator

**Preconditions:**

* Student preferences are collected via a Google Form or Microsoft Form.
* The data is available in an Excel sheet or similar format.

**Main Success Scenario:**

1. The administrator logs into the application.
2. The administrator uploads the Excel sheet containing student preferences into the application.
3. The system processes the data, applying the department's eligibility criteria (subjects, GPA, capacity).
4. The system automatically assigns students to departments based on their preferences and eligibility.
5. The system generates an output file (e.g., Excel sheet) listing students and their assigned departments.
6. The administrator downloads the output file for further use.

**Alternatives:**

* **A1. Invalid or Corrupted Data File:**
  * 2a. The system detects an invalid or corrupted data file.
  * 2b. The system notifies the administrator of the issue and requests a valid file.
  * 2c. Use case ends.
* **A2. System Error During Processing:**
  * 4a. The system encounters an error during data processing.
  * 4b. The system logs the error and notifies the administrator.
  * 4c. Use case ends.

#### 1.2: Adding a New Program to the System

**Actors:**

* Administrator

**Preconditions:**

* The administrator has access to the application with administrative privileges.

**Main Success Scenario:**

1. The administrator logs into the application.
2. The administrator navigates to the "Manage Programs" section.
3. The administrator selects the option to add a new program.
4. The system prompts the administrator to enter details for the new program (e.g., name, eligibility criteria, capacity).
5. The administrator enters the required information and submits the form.
6. The system saves the new program and updates the list of available programs.
7. The system confirms the successful addition of the new program to the administrator.

**Alternatives:**

* **A1. Missing or Incomplete Information:**
  * 5a. The system detects missing or incomplete information in the form.
  * 5b. The system prompts the administrator to complete all required fields.
  * 5c. Use case resumes at step 5.
* **A2. System Error During Program Addition:**
  * 6a. The system encounters an error while saving the new program.
  * 6b. The system logs the error and notifies the administrator.
  * 6c. Use case ends.

#### 1.3: Updating Eligibility Criteria for Existing Programs

**Actors:**

* Administrator

**Preconditions:**

* The administrator has access to the application with administrative privileges.
* Existing programs are already defined in the system.

**Main Success Scenario:**

1. The administrator logs into the application.
2. The administrator navigates to the "Manage Programs" section.
3. The administrator selects an existing program to update.
4. The system displays the current eligibility criteria for the selected program.
5. The administrator modifies the criteria (e.g., subjects, GPA, capacity) as needed.
6. The administrator submits the changes.
7. The system saves the updated criteria and confirms the changes to the administrator.

**Alternatives:**

* **A1. Invalid Criteria Input:**
  * 5a. The system detects invalid input for the criteria.
  * 5b. The system prompts the administrator to correct the input.
  * 5c. Use case resumes at step 5.

#### 1.4: Data Backup and Recovery

**Actors:**

* Administrator

**Preconditions:**

* The system is operational and contains data that needs to be backed up.

**Main Success Scenario:**

1. The administrator logs into the application.
2. The administrator navigates to the "Data Management" section.
3. The administrator selects the option to perform a data backup.
4. The system compiles all relevant data into a backup file.
5. The system prompts the administrator to choose a location to save the backup file.
6. The administrator selects a location and confirms the backup.
7. The system saves the backup file and confirms successful completion to the administrator.

**Recovery Scenario:**

1. The administrator logs into the application.
2. The administrator navigates to the "Data Management" section.
3. The administrator selects the option to restore data from a backup.
4. The system prompts the administrator to select a backup file.
5. The administrator selects the backup file and confirms the restoration.
6. The system restores the data and confirms successful completion to the administrator.

**Alternatives:**

* **A1. Backup Process Error:**
  * 4a. The system encounters an error during the backup process.
  * 4b. The system logs the error and notifies the administrator.
  * 4c. Use case ends.

#### 1.5: User Access Management

**Actors:**

* System Administrator

**Preconditions:**

* The system has multiple users with varying access needs.

**Main Success Scenario:**

1. The system administrator logs into the application.
2. The administrator navigates to the "User Management" section.
3. The administrator selects the option to add or modify user access.
4. The system displays a list of current users and their access levels.
5. The administrator selects a user to modify or adds a new user.
6. The administrator assigns or updates the user's access level and permissions.
7. The administrator submits the changes.
8. The system saves the changes and confirms successful completion to the administrator.

**Alternatives:**

* **A1. Invalid User Information:**
  * 6a. The system detects invalid user information.
  * 6b. The system prompts the administrator to correct the information.
  * 6c. Use case resumes at step 6.

#### 1.6: Generating Reports for Department Allocation

**Actors:**

* Administrator, Department Head

**Preconditions:**

* The system has processed student preferences and assigned them to departments.

**Main Success Scenario:**

1. The administrator logs into the application.
2. The administrator navigates to the "Reports" section.
3. The administrator selects the option to generate a report for department allocations.
4. The system compiles data on student assignments, including statistics like the number of students per department, average GPA, and unmet preferences.
5. The system generates a detailed report in a chosen format (e.g., PDF, Excel).
6. The administrator downloads the report for distribution to department heads or for record-keeping.

**Alternatives:**

* **A1. No Data Available:**
  * 4a. The system detects that no data is available for report generation.
  * 4b. The system notifies the administrator and suggests checking the data processing status.
  * 4c. Use case ends.

#### 1.7: Sending Notifications to Department Heads

**Actors:**

* Administrator, Department Head

**Preconditions:**

* The system has processed student preferences and assigned them to departments.

**Main Success Scenario:**

1. The administrator logs into the application.
2. The administrator navigates to the "Notifications" section.
3. The administrator selects the option to send notifications to department heads.
4. The system automatically generates notifications with details of student assignments and any relevant statistics.
5. The system sends notifications via email to department heads.
6. The system confirms successful delivery of notifications to the administrator.

**Alternatives:**

* **A1. Notification Delivery Failure:**
  * 5a. The system encounters an error while sending notifications.
  * 5b. The system logs the error and notifies the administrator.
  * 5c. Use case ends.

#### 1.8: Sending Notifications to Students

**Actors:**

* Administrator, Student

**Preconditions:**

* The system has processed student preferences and assigned them to departments.
* Students have registered their academic email addresses in the system.

**Main Success Scenario:**

1. The administrator logs into the application.
2. The administrator navigates to the "Notifications" section.
3. The administrator selects the option to send notifications to students.
4. The system automatically generates notifications with details of department assignments.
5. The system sends notifications via email to students, informing them of their department assignments.
6. The system confirms successful delivery of notifications to the administrator.

**Alternatives:**

* **A1. Notification Delivery Failure:**
  * 5a. The system encounters an error while sending notifications.
  * 5b. The system logs the error and notifies the administrator.
  * 5c. Use case ends.
