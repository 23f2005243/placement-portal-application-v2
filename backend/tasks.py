from celery_worker import celery_app
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import smtplib 
from flask import render_template
from models import User, Student, Company, Placement_Drive, Application

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025 #for MailHog
SENDER_ADDRESS='anjalichourasia01@gmail.com'
SENDER_PASSWORD=''

def send_email(to_address,subject,message,content="text",attachment=None):
    msg = MIMEMultipart()
    msg['To']=to_address
    msg['From']=SENDER_ADDRESS
    msg['Subject']=subject
    if content == "html":
        msg.attach(MIMEText(message,'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))

    if attachment:
        with open(attachment,"rb") as a:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(a.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment: filename={attachment}")
        msg.attach(part)          

    s = smtplib.SMTP(host=SERVER_SMTP_HOST, port=SERVER_SMTP_PORT )
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True


from datetime import datetime
from sqlalchemy import func
@celery_app.task
def send_monthly_report():
    admin = User.query.filter_by(utype='admin').first()
    if not admin:
        return "No admin user found"
    
    current_month = datetime.now().strftime("%Y-%m")
    total_drives = Placement_Drive.query.filter(
    func.substr(Placement_Drive.application_deadline, 1, 7) == current_month,
    Placement_Drive.status == "Approved"
).count()
    total_applied = Application.query.filter(
    func.substr(Application.application_date, 1, 7) == current_month
).count()
    total_selected = Application.query.filter(
    func.substr(Application.application_date, 1, 7) == current_month,
    Application.status == "Selected"
).count()

    applications = Application.query.filter(
    func.substr(Application.application_date, 1, 7) == current_month
).all()
    application_data = []
    for application in applications:
        student = Student.query.get(application.sid)
        drive = Placement_Drive.query.get(application.did)
        if not student or not drive:
            continue
        company = Company.query.get(drive.cid)
        application_data.append({
            "student_id": student.sid,
            "student_name": student.sname,
            "company_name": company.cname if company else "",
            "job_title": drive.job_title,
            "status": application.status,
            "application_date": application.application_date
    })

    html = render_template('monthly_report.html', month=datetime.now().strftime("%B %Y"),
        total_drives=total_drives,
        total_applied=total_applied,
        total_selected=total_selected, applications=application_data)
    send_email(admin.email, "Monthly Placement Report", html, content="html")
   
    return "Monthly placement report sent to admin."
    

from datetime import date, timedelta
@celery_app.task
def send_daily_reminder():  
    reminder_date = date.today() + timedelta(days=1)
    upcoming_drives = Placement_Drive.query.filter(Placement_Drive.application_deadline == reminder_date and Placement_Drive.status == "Approved").all()
    active_students = Student.query.filter_by(status="Activated").all()
    for drive in upcoming_drives:
        for student in active_students:
            already_applied = Application.query.filter_by(sid=student.sid, did=drive.did).first()
            if already_applied:
                continue
            user = User.query.get(student.sid)
            send_email(user.email, "Application Deadline Reminder", f"""
Dear {student.sname},

This is a gentle reminder for the following placement drive whose application deadline is tomorrow.

Company: {drive.company.cname}
Job Title: {drive.job_title}
Salary: {drive.salary}
Location: {drive.location}
Interview Type: {drive.interview_type}
Deadline: {drive.application_deadline}

Please submit your application before the deadline if you are interested in the drive.

Regards,
Placement Portal
""",
                content="plain"
            )
    return "Daily reminder sent to students with active account"
    

@celery_app.task
def export_applications_report(student_id):
    user = User.query.get(student_id)
    applications = Application.query.filter_by(sid=student_id).all()
    application_data = []
    total_shortlisted = 0
    total_selected = 0
    total_rejected = 0
    for application in applications:
        drive = Placement_Drive.query.get(application.did)
        company = Company.query.get(drive.cid)
        if application.status == "Shortlisted":
            total_shortlisted += 1
        elif application.status == "Selected":
            total_selected += 1
        elif application.status == "Rejected":
            total_rejected += 1
        application_data.append({
            'sid': student_id,
            'cname': company.cname,
            'job_title': drive.job_title,
            'status': application.status,
            'application_date': application.application_date
        })
    
    html = render_template('export.html',applications=application_data,username=user.username,total_applications=len(application_data),
    total_shortlisted=total_shortlisted,
        total_selected=total_selected,
        total_rejected=total_rejected)

    send_email(user.email,"Your Placement Application Report",html,content="html")

    return "Application report sent to student."  
        