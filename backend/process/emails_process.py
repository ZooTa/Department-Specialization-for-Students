import smtplib
import ssl
from email.message import EmailMessage


def load_and_fill_template(name, department, template_path="email_template.html"):
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    return template.replace("{{name}}", str(name)).replace("{{department}}", str(department))


class EmailSender:

    def __init__(self, student_service, sender_email, password,
                 smtp_host="smtp.gmail.com", smtp_port=465):
        self.student_service = student_service
        self.sender_email = sender_email
        self.password = password
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

    def send_email(self, recipient_email, html_content):
        msg = EmailMessage()
        msg["Subject"] = "إخطار بالقبول في القسم"
        msg["From"] = self.sender_email
        msg["To"] = recipient_email
        msg.set_content("هذا البريد يحتوي على نسخة HTML. يرجى استخدام عميل بريد يدعمه.")
        msg.add_alternative(html_content, subtype="html")

        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=context) as smtp:
                smtp.login(self.sender_email, self.password)
                smtp.send_message(msg)
            print(f"[+] Sent to {recipient_email}")
        except Exception as e:
            print(f"[!] Failed to send email to {recipient_email}: {e}")

    def send_batch_emails(self, template_path="backend/process/email_template.html"):
        students = self.student_service.get_all()
        for student in students:
            name = student.name
            email = student.email
            department = (
                student.assignment_results[0].result
                if student.assignment_results else "Unknown"
            )

            print(f"Sending email to {name} ({email}) in {department} department...")
            html_content = load_and_fill_template(name, department, template_path)
            self.send_email(email, html_content)

#
#
#
# def send_email(sender_email, password, recipient_email, subject, html_content, smtp_host="smtp-mail.outlook.com",
#                smtp_port=587):
#     message = MIMEMultipart("alternative")
#     message["Subject"] = subject
#     message["From"] = sender_email
#     message["To"] = recipient_email
#
#     message.attach(MIMEText(html_content, "html"))
#
#     smtp = smtplib.SMTP(smtp_host, smtp_port)
#     smtp.starttls()
#     smtp.login(sender_email, password)
#     smtp.sendmail(sender_email, recipient_email, message.as_string())
#     smtp.quit()
#
#     print(f"[+] Sent to {recipient_email}")
#
#
# def send_email_with_attachment(sender_email, recipient_email, html_file, attachment_path, smtp_host, smtp_port):
#     password = getpass.getpass(f"Enter password for {sender_email}: ")
#
#     message = MIMEMultipart("alternative")
#     message["Subject"] = "Your Weekly Update"
#     message["From"] = sender_email
#     message["To"] = recipient_email
#
#     # Attach HTML
#     with open(html_file, "r") as f:
#         html = f.read()
#     message.attach(MIMEText(html, "html"))
#
#     # Attach file
#     with open(attachment_path, "rb") as f:
#         part = MIMEBase("application", "octet-stream")
#         part.set_payload(f.read())
#     encoders.encode_base64(part)
#     part.add_header("Content-Disposition", f"attachment; filename={attachment_path}")
#     message.attach(part)
#
#     # Send
#     smtp = smtplib.SMTP(smtp_host, smtp_port)
#     smtp.ehlo()
#     smtp.starttls()
#     smtp.login(sender_email, password)
#     smtp.sendmail(sender_email, recipient_email, message.as_string())
#     smtp.quit()
#     print("Email sent successfully!")
#
#
# # Example usage:
# send_email_with_attachment(
#     sender_email="youremail@example.com",
#     recipient_email="receiver@example.com",
#     html_file="dataframe.html",
#     attachment_path="output.xlsx",
#     smtp_host="smtp.gmail.com",  # or smtp-mail.outlook.com
#     smtp_port=587
# )
