from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, User, Company, Student, Placement_Drive, Application
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_caching import Cache

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'


CORS(app)

db.init_app(app)

jwt = JWTManager(app)

cache = Cache(app)


@app.route('/api/company/register', methods=['POST'])
def company_register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    elif User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    else:
        
        user = User(
            username=data['username'],
            email=data['email'],        
            password=generate_password_hash(data['password']),
            utype=data['utype']
        )
        db.session.add(user)
        db.session.commit()

        
        company = Company(
            cid=user.uid,
            username=user.username,
            cname=data.get('cname'),
            cabout=data.get('cabout'),
            clocation=data.get('clocation'),
            hr_contact=data.get('hr_contact'),
            c_website=data.get('c_website'),
            approval_status='Pending'
        )
        db.session.add(company) 
        db.session.commit()

    return jsonify({'message': 'Company registered successfully'}), 200


@app.route('/api/student/register', methods=['POST'])
def student_register():
    data = request.get_json()

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    elif User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    else:
        user = User(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            utype=data['utype']
        )
        db.session.add(user)
        db.session.commit()

        student = Student(
            sid=user.uid,
            username=user.username,
            sname=data.get('sname'),
            sdepartment=data.get('sdepartment'),
            gpa=data.get('gpa'),
            yog=data.get('yog'),
            contact=data.get('contact'),
            resume=data.get('resume')
        )
        db.session.add(student)
        db.session.commit()

    return jsonify({'message': 'Student registered successfully'}), 200


@app.route('/api/company/login', methods=['POST'])
def company_login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    company = Company.query.filter_by(cid=user.uid).first()
    if user and check_password_hash(user.password, data['password']) and user.utype == 'company':
        if company.approval_status != "Approved":
            return jsonify({"message": "Your account is not yet approved by the admin. Please wait"}), 403
        access_token = create_access_token(identity=str(user.uid), additional_claims={'utype': user.utype})
        return jsonify({'message': 'Company login successful', 'data': {'username': user.username, 'email': user.email, 'utype': user.utype, 'access_token': access_token}}), 200
    else:
        return jsonify({'message': 'Invalid company credentials'}), 401


@app.route('/api/company/<int:company_id>', methods=['GET'])
@jwt_required()
def get_company(company_id):
    company = Company.query.filter_by(cid=company_id).first()
    if not company:
        return jsonify({'message': 'Company not found'}), 404
    
    return jsonify({
        'cid': company.cid,
        'cname': company.cname,
        'c_website': company.c_website,
        'clocation': company.clocation,
        'hr_contact': company.hr_contact,
        'approval_status': company.approval_status,
        'cabout': company.cabout
    }), 200


@app.route('/api/student/login', methods=['POST'])
def student_login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    student = Student.query.filter_by(sid=user.uid).first()
    if user and check_password_hash(user.password, data['password']) and user.utype == 'student':
        if student.status != "Activated":
            return jsonify({"message": "Your account has been deactivated by the admin."}), 403
        access_token = create_access_token(identity=str(user.uid), additional_claims={'utype': user.utype})
        return jsonify({'message': 'Student login successful', 'data': {'username': user.username, 'email': user.email, 'utype': user.utype, 'access_token': access_token}}), 200
    else:
        return jsonify({'message': 'Invalid student credentials'}), 401


@app.route('/api/student/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    
    return jsonify({
        'sid': student.sid,
        'sname': student.sname,
        'sdepartment': student.sdepartment,
        'gpa': student.gpa,
        'yog': student.yog,
        'contact': student.contact,
        'resume': student.resume,
        'status': student.status
    }), 200


@app.route('/api/student/edit-profile/<int:student_id>', methods=['PUT'])
@jwt_required()
def edit_student_profile(student_id):
    try:
        uid = int(get_jwt_identity())
        student = Student.query.get(student_id)
        
        if not student:
            return jsonify({'message': 'Student not found'}), 404
        
        if student.sid != uid:
            return jsonify({'message': 'Unauthorized: Can only edit your own profile'}), 403
        
        if student.status != 'Activated':
            return jsonify({'message': 'Account is deactivated'}), 403
        
        data = request.get_json()
        if 'gpa' in data:
            student.gpa = data['gpa']
        if 'contact' in data:
            student.contact = data['contact']
        if 'resume' in data:
            student.resume = data['resume']

        db.session.commit()
        return jsonify({'message': 'Student profile updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500



@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']) and user.utype == 'admin':
        access_token = create_access_token(identity=str(user.uid), additional_claims={'utype': user.utype})
        return jsonify({'message': 'Admin login successful', 'data': {'username': user.username, 'email': user.email, 'utype': user.utype, 'access_token': access_token}}), 200
    else:
        return jsonify({'message': 'Invalid admin credentials'}), 401
    

@app.route('/api/admin/dashboard-stats', methods=['GET'])
@jwt_required()
def admin_dashboard_stats():

    if get_jwt().get('utype') != 'admin':
        return jsonify({"message": "Admin access required"}), 403

    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_drives = Placement_Drive.query.count()
    total_applications = Application.query.count()

    return jsonify({
        "total_students": total_students,
        "total_companies": total_companies,
        "total_drives": total_drives,
        "total_applications": total_applications
    }), 200


@app.route('/api/create/drive', methods=['POST'])
@jwt_required()
def create_drive():
    if get_jwt().get('utype') != 'company':
        return jsonify({'message': 'Company access required'}), 403
    if approval_status := Company.query.filter_by(cid=get_jwt_identity()).first().approval_status != 'Approved':
        return jsonify({'message': 'Company not approved.'}), 403
    
    data = request.get_json()
    drive = Placement_Drive(
        dname=data['dname'],
        cid=get_jwt_identity(),
        job_title=data['job_title'],
        job_description=data['job_description'],
        eligible_dept=data['eligible_dept'],
        min_gpa=data['min_gpa'],
        eligible_yog=data['eligible_yog'],
        salary=data['salary'],
        location=data['location'],
        interview_type=data['interview_type'],
        application_deadline=data['application_deadline'],
        
    )
    db.session.add(drive)
    db.session.commit()

    return jsonify({'message': 'Placement drive created successfully'}), 200


@app.route('/api/company/view-drive/<int:drive_id>', methods=['GET'])
@jwt_required()
#@cache.cached(timeout=60)
def company_view_drive(drive_id):
    drive = Placement_Drive.query.filter_by(did=drive_id).first()
    
    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    return jsonify({
    'did': drive.did,
    'dname': drive.dname,
    'job_title': drive.job_title,
    'job_description': drive.job_description,
    'eligible_dept': drive.eligible_dept,
    'min_gpa': drive.min_gpa,
    'eligible_yog': drive.eligible_yog,
    'salary': drive.salary,
    'location': drive.location,
    'interview_type': drive.interview_type,
    'application_deadline': drive.application_deadline,
    'status': drive.status
})


@app.route('/api/update/drive/<int:drive_id>', methods=['PUT'])
@jwt_required()
def update_drive(drive_id):
    if get_jwt().get('utype') != 'company':
        return jsonify({'message': 'Company access required'}), 403

    drive = Placement_Drive.query.get(drive_id)
    # drive = Placement_Drive.query.filter_by(did=drive_id).first()
    if not drive:
        return jsonify({'message': 'Placement drive not found'}), 404

    data = request.get_json()
    drive.dname = data.get('dname', drive.dname)
    drive.job_title = data.get('job_title', drive.job_title)
    drive.job_description = data.get('job_description', drive.job_description)
    drive.eligible_dept = data.get('eligible_dept', drive.eligible_dept)
    drive.min_gpa = data.get('min_gpa', drive.min_gpa)
    drive.eligible_yog = data.get('eligible_yog', drive.eligible_yog)
    drive.salary = data.get('salary', drive.salary)
    drive.location = data.get('location', drive.location)
    drive.interview_type = data.get('interview_type', drive.interview_type)
    drive.application_deadline = data.get('application_deadline', drive.application_deadline)

    db.session.commit()

    return jsonify({'message': 'Placement drive updated successfully'}), 200


@app.route('/api/delete/drive/<int:drive_id>', methods=['PUT'])
@jwt_required()
def delete_drive(drive_id):
    if get_jwt().get('utype') != 'company':
        return jsonify({'message': 'Company access required'}), 403

    drive = Placement_Drive.query.get(drive_id)
    if not drive or drive.is_deleted:
        return jsonify({'message': 'Placement drive not found'}), 404

    drive.is_deleted = True
    db.session.commit()

    return jsonify({'message': 'Placement drive deleted successfully'}), 200


@app.route('/api/get/registered-companies', methods=['GET'])
@jwt_required()
#@cache.cached(timeout=60)
def get_registered_companies():
    if get_jwt().get('utype') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403 
    
    companies = Company.query.filter_by(approval_status='Approved').all()
    
    data = []
    for company in companies:
        company_data = {
            'cid': company.cid,
            'cname': company.cname,
            'c_website': company.c_website,
            'clocation': company.clocation,
            'approval_status': company.approval_status
        }
        data.append(company_data)
        
    return jsonify(data)

          
@app.route('/api/get/registered-students', methods=['GET'])
@jwt_required()
#@cache.cached(timeout=60)
def get_registered_students():
    if get_jwt().get('utype') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403 
    
    students = Student.query.all()
    
    data = []
    for student in students:
        student_data = {
            'sid': student.sid,
            'sname': student.sname,
            'sdepartment': student.sdepartment,
            'yog': student.yog,
            'contact': student.contact,
            'status': student.status
        }
        data.append(student_data)
        
    return jsonify(data)


@app.route('/api/admin/<int:student_id>/activate/student', methods=['PUT'])
@jwt_required()
def activate_student(student_id):
    if get_jwt().get('utype') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403 
    
    student = Student.query.filter_by(sid = student_id).first()
    if not student or student.status == 'Activated':
        return jsonify({'message': 'Student not found or already activated'}), 404
    
    student.status = 'Activated'
    db.session.commit()
    
    return jsonify({'message': 'Student account activated successfully'}), 200


@app.route('/api/admin/<int:student_id>/deactivate/student', methods=['PUT'])
@jwt_required()
def deactivate_student(student_id):
    if get_jwt().get('utype') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403 
    
    student = Student.query.filter_by(sid = student_id).first()
    if not student or student.status == 'Dectivated':
        return jsonify({'message': 'Student not found or already deactivated'}), 404
    
    student.status = 'Deactivated'
    db.session.commit()
    
    return jsonify({'message': 'Student account deactivated successfully'}), 200


@app.route('/api/get/company-applications', methods=['GET'])
@jwt_required()
def get_company_applications():
    if get_jwt().get('utype') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403 
    
    companies = Company.query.filter_by(approval_status='Pending').all()
    
    data = []
    for company in companies:
        company_data = {
            'cid': company.cid,
            'cname': company.cname,
            'c_website': company.c_website,
            'clocation': company.clocation,
            'approval_status': company.approval_status
        }
        data.append(company_data)
        
    return jsonify(data)


@app.route('/api/admin/<int:company_id>/approve/company', methods=['PUT'])
@jwt_required()
def approve_company(company_id):
    if get_jwt().get('utype') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403 
    
    company = Company.query.filter_by(cid = company_id).first()
    if not company:
        return jsonify({'message': 'Company not found'}), 404
    
    company.approval_status = 'Approved'
    db.session.commit()
    
    return jsonify({'message': 'Company approved successfully'}), 200


@app.route('/api/admin/<int:company_id>/reject/company', methods=['PUT'])
@jwt_required()
def reject_company(company_id):
    if get_jwt().get('utype') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403 
    
    company = Company.query.filter_by(cid = company_id).first()
    if not company:
        return jsonify({'message': 'Company not found'}), 404
    
    company.approval_status = 'Rejected'
    db.session.commit()
    
    return jsonify({'message': 'Company rejected successfully'}), 200


@app.route('/api/admin/<int:company_id>/blacklist/company', methods=['PUT'])
@jwt_required()
def blacklist_company(company_id):
    if get_jwt().get('utype') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403 
    
    company = Company.query.filter_by(cid = company_id).first()
    if not company:
        return jsonify({'message': 'Company not found'}), 404
    
    company.approval_status = 'Blacklisted'
    db.session.commit()
    
    return jsonify({'message': 'Company blacklisted successfully'}), 200


@app.route('/api/get/placement-drives', methods=['GET'])
@jwt_required()
def get_placement_drives():
    if get_jwt().get('utype') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403 
    
    drives = Placement_Drive.query.filter_by(is_deleted=False).all()
    
    data = []
    for drive in drives:
        drive_data = {
            'did': drive.did,
            'dname': drive.dname,
            'cname': drive.company.cname if drive.company else None,
            'job_title': drive.job_title,
            'status': drive.status
        }
        data.append(drive_data)
        
    return jsonify(data)


@app.route('/api/admin/view-drive/<int:drive_id>', methods=['GET'])
@jwt_required()
def admin_view_drive(drive_id):
    drive = Placement_Drive.query.filter_by(did=drive_id, is_deleted=False).first()
    
    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    return jsonify({
    'did': drive.did,
    'dname': drive.dname,
    'job_title': drive.job_title,
    'job_description': drive.job_description,
    'eligible_dept': drive.eligible_dept,
    'min_gpa': drive.min_gpa,
    'eligible_yog': drive.eligible_yog,
    'salary': drive.salary,
    'location': drive.location,
    'interview_type': drive.interview_type,
    'application_deadline': drive.application_deadline,
    'status': drive.status
})


@app.route('/api/admin/<int:drive_id>/approve/drive', methods=['PUT'])
@jwt_required()
def approve_drive(drive_id):
    if get_jwt().get('utype') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403 
    
    drive = Placement_Drive.query.filter_by(did = drive_id,is_deleted=False).first()
    if not drive:
        return jsonify({'message': 'Placement drive not found'}), 404
    
    drive.status = 'Approved'
    db.session.commit()
    
    return jsonify({'message': 'Placement drive approved successfully'}), 200


@app.route('/api/admin/<int:drive_id>/reject/drive', methods=['PUT'])
@jwt_required()
def reject_drive(drive_id):
    if get_jwt().get('utype') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403 
    
    drive = Placement_Drive.query.filter_by(did = drive_id,is_deleted=False).first()
    if not drive:
        return jsonify({'message': 'Placement drive not found'}), 404
    
    drive.status = 'Rejected'
    db.session.commit()
    
    return jsonify({'message': 'Placement drive rejected successfully'}), 200


@app.route('/api/get/student-applications', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60)
def get_student_applications():
    if get_jwt().get('utype') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403

    applications = Application.query.all()

    data = []
    for application in applications:
        student = application.student
        drive = application.drive
        company = drive.company if drive else None

        app_data = {
            'aid': application.aid,
            'student_name': student.sname if student else None,
            'drive_name': drive.dname if drive else None,
            'company_name': company.cname if company else None,
            'application_date': application.application_date,
            'status': application.status
        }
        data.append(app_data)

    return jsonify(data)


@app.route('/api/admin/view-application/<int:application_id>', methods=['GET'])
@jwt_required()
def admin_view_application(application_id):
    # Allow only admin
    if get_jwt().get('utype') != 'admin':
        return jsonify({"message": "Admin access required"}), 403

    application = Application.query.filter_by(aid=application_id).first()

    if not application:
        return jsonify({"message": "Application not found"}), 404

    student = application.student
    drive = application.drive
    company = drive.company if drive else None

    return jsonify({
        "aid": application.aid,
        "sname": student.sname if student else None,
        "sdepartment": student.sdepartment if student else None,
        "cname": company.cname if company else None,
        "dname": drive.dname if drive else None,
        "job_title": drive.job_title if drive else None,
        "salary": drive.salary if drive else None,
        "status": application.status,
        "resume": application.resume
    }), 200


@app.route('/api/get/company/drives', methods=['GET'])
@jwt_required()
def get_company_drives():
    if get_jwt().get('utype') != 'company':
        return jsonify({'message': 'Company access required'}), 403 
    company_id = get_jwt_identity()
    drives = Placement_Drive.query.filter_by(cid = company_id).all()
    
    data = []
    for drive in drives:
        drive_data = {
            'cid': get_jwt_identity(),
            'did': drive.did,
            'dname': drive.dname,
            'job_title': drive.job_title,
            'application_deadline': drive.application_deadline,
            'numOfApplicants': len(drive.applications),
            'status': drive.status,
            'deletion_status': drive.is_deleted
        }
        data.append(drive_data)
        
    return jsonify(data)


@app.route('/api/company/view-applications/<int:drive_id>', methods=['GET'])
@jwt_required()
#@cache.cached(timeout=60)
def company_view_applications(drive_id):

    if get_jwt().get('utype') != 'company':
        return jsonify({"message": "Company access required"}), 403

    company_id = get_jwt_identity()

    drive = Placement_Drive.query.filter_by(did=drive_id, cid=company_id,is_deleted=False).first()

    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    applications = []

    for application in drive.applications:
        student = application.student

        applications.append({
            "aid": application.aid,
            "sid": student.sid,
            "sname": student.sname,
            "status": application.status
        })

    return jsonify({
        "drive": {
            "did": drive.did,
            "dname": drive.dname,
            "job_title": drive.job_title,
            
        },
        "applications": applications
    }), 200


@app.route('/api/company/review-application/<int:application_id>', methods=['GET'])
@jwt_required()
#@cache.cached(timeout=60)
def company_review_application(application_id):

    if get_jwt().get('utype') != 'company':
        return jsonify({"message": "Company access required"}), 403

    company_id = int(get_jwt_identity())
    application = Application.query.filter_by(aid=application_id).first()

    if not application:
        return jsonify({"message": "Application not found"}), 404

    drive = application.drive

    if drive.cid != company_id:
        return jsonify({"message": "Unauthorized"}), 403

    student = application.student

    return jsonify({
        "aid": application.aid,
        "sname": student.sname,
        "sdepartment": student.sdepartment,
        "dname": drive.dname,
        "job_title": drive.job_title,
        "status": application.status,
        "resume": application.resume
    }), 200


@app.route('/api/company/update-selection-status/<int:application_id>', methods=['PUT'])
@jwt_required()
def update_selection_status(application_id):

    if get_jwt().get('utype') != 'company':
        return jsonify({"message": "Company access required"}), 403

    company_id = int(get_jwt_identity())

    application = Application.query.filter_by(aid=application_id).first()

    if not application:
        return jsonify({"message": "Application not found"}), 404

    drive = application.drive

    # Ensure the logged-in company owns this drive
    if drive.cid != company_id:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()

    allowed_status = ["Applied", "Shortlisted", "Selected", "Rejected"]

    if data.get("status") not in allowed_status:
        return jsonify({"message": "Invalid status"}), 400

    application.status = data["status"]

    db.session.commit()

    return jsonify({
        "message": "Selection status updated successfully."
    }), 200


@app.route('/api/get/organizations', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60)
def get_organizations():
    if get_jwt().get('utype') != 'student':
        return jsonify({'message': 'Student access required'}), 403 
    
    companies = Company.query.filter_by(approval_status='Approved').all()
    
    data = []
    for company in companies:
        company_data = {
            'cid': company.cid,
            'cname': company.cname,
            'c_website': company.c_website,
            'clocation': company.clocation
        }
        data.append(company_data)
        
    return jsonify(data)


@app.route('/api/student/get/applied-drives', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60)
def get_applied_drives():
    if get_jwt().get('utype') != 'student':
        return jsonify({'message': 'Student access required'}), 403 
    
    student = Student.query.filter_by(sid=get_jwt_identity()).first()
    if not student:
        return jsonify({'message': 'Student not found'}), 404

    applications = Application.query.filter(Application.sid == get_jwt_identity(), Application.status == "Applied").all()
    data = []
    for application in applications:
        drive = Placement_Drive.query.filter_by(did=application.did,is_deleted=False).first()

        if drive:
            company = Company.query.filter_by(cid=drive.cid).first()
        else:
            company = None

        app_data = {
            "sid": get_jwt_identity(),
            "aid": application.aid,
            "did": drive.did,
            'drive_name': drive.dname if drive else None,
            'company_name': company.cname if company else None,
            'application_date': application.application_date,
            'status': application.status
        }
        data.append(app_data)

    return jsonify(data), 200


@app.route('/api/student/view-company/<int:company_id>', methods=['GET'])
@jwt_required()
#@cache.cached(timeout=60)
def student_view_company(company_id):
    company = Company.query.filter_by(cid=company_id).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    drives = Placement_Drive.query.filter(Placement_Drive.cid == company_id, Placement_Drive.status == 'Approved', Placement_Drive.is_deleted == False).all()

    drive_details = []

    for drive in drives:
        drive_details.append({
            "did": drive.did,
            "dname": drive.dname,
            "job_title": drive.job_title,
            "application_deadline": drive.application_deadline,
            "status": drive.status
        })

    return jsonify({
        "company": {
            "cid": company.cid,
            "cname": company.cname,
            "c_website": company.c_website,
            "cabout": company.cabout,
            "hr_contact": company.hr_contact
        },
        "drives": drive_details
    })


@app.route('/api/student/view-drive/<int:drive_id>', methods=['GET'])
@jwt_required()
#@cache.cached(timeout=60)
def student_view_drive(drive_id):
    drive = Placement_Drive.query.filter_by(did=drive_id, is_deleted=False).first()
    
    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    company = Company.query.filter_by(cid=drive.cid).first()

    return jsonify({
    'did': drive.did,
    'dname': drive.dname,
    "cname": drive.company.cname if company else None,
    'job_title': drive.job_title,
    'job_description': drive.job_description,
    'eligible_dept': drive.eligible_dept,
    'min_gpa': drive.min_gpa,
    'eligible_yog': drive.eligible_yog,
    'salary': drive.salary,
    'location': drive.location,
    'interview_type': drive.interview_type,
    'application_deadline': drive.application_deadline,
    'status': drive.status
})


@app.route('/api/student/view-applied-drive/<int:drive_id>', methods=['GET'])
@jwt_required()
#@cache.cached(timeout=60)
def student_view_applied_drive(drive_id):

    drive = Placement_Drive.query.filter_by(did=drive_id,is_deleted=False).first()

    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    return jsonify({
        "did": drive.did,
        "dname": drive.dname,
        "cname": drive.company.cname if drive.company else None,
        "job_title": drive.job_title,
        "job_description": drive.job_description,
        "eligible_dept": drive.eligible_dept,
        "min_gpa": drive.min_gpa,
        "eligible_yog": drive.eligible_yog,
        "salary": drive.salary,
        "location": drive.location,
        "interview_type": drive.interview_type
    }), 200


@app.route('/api/get/student/my-history', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60)
def get_my_history():
    if get_jwt().get('utype') != 'student':
        return jsonify({'message': 'Student access required'}), 403 
    
    student_id = get_jwt_identity()
    applications = Application.query.filter(Application.sid == student_id, Application.status != "Applied").all()

    data = []
    for application in applications:
        drive = application.drive
        company = drive.company if drive else None

        app_data = {
            'aid': application.aid,
            'drive_name': drive.dname if drive else None,
            'company_name': company.cname if company else None,
            'job_title': drive.job_title if drive else None,
            'application_type': application.atype,
            'interview_type': drive.interview_type if drive else None,
            'status': application.status
        }
        data.append(app_data)

    return jsonify(data)


from datetime import date
@app.route('/api/student/apply-drive/<int:drive_id>', methods=['GET', 'POST'])
@jwt_required()
def apply_drive(drive_id):
    student_id = get_jwt_identity()
    student = Student.query.filter_by(sid=student_id).first()
    if not student:
        return jsonify({"message": "Student not found"}), 404
    drive = Placement_Drive.query.filter_by(did=drive_id,is_deleted=False).first()
    if not drive:
        return jsonify({"message": "Drive not found"}), 404
    company = Company.query.filter_by(cid=drive.cid).first() 
    if request.method == "GET":
        return jsonify({
            "did": drive.did,
            "dname": drive.dname,
            "sid": student.sid,
            "sname": student.sname,
            "cname": company.cname if company else "",
            "atype": "Direct",
            "application_date": str(date.today()),
            "resume": student.resume if student.resume else ""
        }), 200
    data = request.get_json()
    existing = Application.query.filter_by(sid=student.sid, did=drive.did).first()
    if existing:
        return jsonify({"message": "You have already applied for this drive."}), 400
    application = Application(
        sid=student.sid,
        did=drive.did,
        atype=data.get("atype"),
        gpa=student.gpa,
        yog=student.yog,
        application_date=data.get("application_date"),
        resume=data.get("resume"),
        status="Applied"
    )
    db.session.add(application)
    db.session.commit()
    return jsonify({"message": "Application submitted successfully."}), 201


@app.route('/api/export/applications', methods=['GET'])
@jwt_required()
def export_applications():
    if get_jwt().get('utype') != 'student':
        return jsonify({'message': 'Student access required'}), 403
    student_id = get_jwt_identity()
    from tasks import export_applications_report
    export_applications_report.delay(student_id)
    return jsonify({'message': 'Your placement application report is being generated and will be sent to your email shortly.'}), 200


@app.route('/api/student/summary', methods=['GET'])
@jwt_required()
def student_summary():
    student_id = get_jwt_identity()
    applications = Application.query.filter_by(sid=student_id).all()
    company_applied = {}
    #Pie Chart
    total_applied = len(applications)
    total_shortlisted = 0
    total_selected = 0
    total_rejected = 0
    for application in applications:
        drive = application.drive  
        company = Company.query.get(drive.cid)
        company_name = company.cname
        if company_name not in company_applied:
            company_applied[company_name] = 1
        else: 
            company_applied[company_name] += 1
        if application.status == "Shortlisted":
            total_shortlisted += 1
        elif application.status == "Selected":
            total_selected += 1
        elif application.status == "Rejected":
            total_rejected += 1  
    #Bar Chart      
    company_names = list(company_applied.keys())
    application_counts = list(company_applied.values())
    return jsonify({
        "company_names": company_names,
        "application_counts": application_counts,
        "total_applied": total_applied,
        "total_shortlisted": total_shortlisted,
        "total_selected": total_selected,
        "total_rejected": total_rejected
    }), 200


@app.route('/api/company/summary', methods=['GET'])
@jwt_required()
def company_summary():
    company_id = get_jwt_identity()
    drives = Placement_Drive.query.filter_by(cid=company_id, status="Approved",is_deleted=False).all()
    drive_summary = {}
    total_drives = len(drives)
    total_applied = 0
    total_selected = 0
    for drive in drives:
        applications = Application.query.filter_by(did=drive.did).all()
        applied = len(applications)
        selected = sum(1 for application in applications if application.status == "Selected")
        drive_summary[drive.dname] = {
            "applied": applied,
            "selected": selected
        }
        total_applied += applied
        total_selected += selected
    drive_names = []
    applied_counts = []
    selected_counts = []

    for drive_name, summary in drive_summary.items():
        drive_names.append(drive_name)
        applied_counts.append(summary["applied"])
        selected_counts.append(summary["selected"])

    return jsonify({
        "drive_names": drive_names,
        "applied_counts": applied_counts,
        "selected_counts": selected_counts,
        "total_drives": total_drives,
        "total_applied": total_applied,
        "total_selected": total_selected
    }), 200


@app.route('/api/admin/summary', methods=['GET'])
@jwt_required()
def admin_summary():
    if get_jwt().get('utype') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    companies = Company.query.filter_by(approval_status = "Approved").all()
    drives_per_company = {}
    applied_selected = {}
    total_drives = 0
    total_applications = 0
    total_selected = 0
    for company in companies:
        company_name = company.cname
        drives = Placement_Drive.query.filter_by(cid=company.cid,is_deleted=False, status="Approved").all()
        drive_count = len(drives)
        drives_per_company[company_name] = drive_count
        applied_selected[company_name] = {
            "applied": 0,
            "selected": 0
        }
        total_drives += drive_count
        for drive in drives:
            applications = Application.query.filter_by(did=drive.did).all()
            applied_selected[company_name]["applied"] += len(applications)
            selected = sum(1 for app in applications if app.status == "Selected")
            applied_selected[company_name]["selected"] += selected
            total_applications += len(applications)
            total_selected += selected
    company_names = list(drives_per_company.keys())
    drive_counts = list(drives_per_company.values())
    applied_counts = []
    selected_counts = []
    for company in company_names:
        applied_counts.append(applied_selected[company]["applied"])
        selected_counts.append(applied_selected[company]["selected"])
    return jsonify({
        "company_names": company_names,
        "drive_counts": drive_counts,
        "applied_counts": applied_counts,
        "selected_counts": selected_counts,
        "total_companies": len(companies),
        "total_drives": total_drives,
        "total_applications": total_applications,
        "total_selected": total_selected
    }), 200


from sqlalchemy import or_
@app.route('/api/admin/search/company', methods=['GET'])
@jwt_required()
def search_company():
    if get_jwt().get('utype') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    query = request.args.get('query', '').strip()
    companies = Company.query.filter(or_(Company.cname.ilike(f'%{query}%'), Company.cid.cast(db.String).ilike(f'%{query}%'))).all()
    data = []
    for company in companies:
        data.append({
            "cid": company.cid,
            "cname": company.cname,
            "c_website": company.c_website,
            "hr_contact": company.hr_contact,
            "clocation": company.clocation,
            "status": company.approval_status
        })
    return jsonify(data), 200


@app.route('/api/admin/search/student', methods=['GET'])
@jwt_required()
def search_student():
    if get_jwt().get('utype') != 'admin':
        return jsonify({'message': 'Admin access required'}), 403
    query = request.args.get('query', '').strip()
    students = Student.query.filter(or_(Student.sname.ilike(f'%{query}%'), Student.sid.cast(db.String).ilike(f'%{query}%'))).all()
    data = []
    for student in students:
        data.append({
            "sid": student.sid,
            "sname": student.sname,
            "sdepartment": student.sdepartment,
            "gpa": student.gpa,
            "yog": student.yog,
            "contact": student.contact,
            "resume": student.resume
        })
    return jsonify(data), 200


@app.route('/api/get/student/eligible-drives', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60)
def get_eligible_drives():
    student_id = get_jwt_identity()
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message":"Student not found"}),404
    drives = Placement_Drive.query.filter_by(status="Approved", is_deleted = False).all()
    eligible_drives = []
    for drive in drives:
        if drive.eligible_dept != "All" and drive.eligible_dept != student.sdepartment:
            continue
        if drive.min_gpa > student.gpa:
            continue
        if drive.eligible_yog != student.yog:
            continue
        eligible_drives.append({
            "did": drive.did,
            "dname": drive.dname,
            "cname": drive.company.cname,
            "job_title": drive.job_title,
            "salary": drive.salary,
            "location": drive.location,
            "application_deadline": drive.application_deadline
        })
    return jsonify(eligible_drives)


@app.route('/api/get-data', methods=['GET'])
@jwt_required()
def get_data():
    data = {
        'uid': 1,
        'message': 'Hello from the backend!',
        'items': [1, 2, 3, 4, 5]
    }
    return jsonify(data)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@gmail.com', password=generate_password_hash('1234'), utype='admin')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)