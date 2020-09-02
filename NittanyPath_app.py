from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from sqlalchemy import String
import datetime

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'

@app.route('/', methods = ['GET', 'POST'])
def login():
    error = None
    login_type = ''
    test_var = request.form.get("login-type")
    #print(test_var)
    if request.method == 'POST':
        #print(test_var)
        if str(test_var) == ('Student' or 'Teaching Assistance'):
            #print('success')
            login_type = 'Students'
        else:
            #print('wanted success')
            login_type = 'Professors'

        result = valid_credentials(login_type,request.form['UserName'],request.form['Password'])
        #print(result,login_type,test_var)
        if result:
            return redirect(url_for(test_var, user = request.form['UserName']))
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error = error)

@app.route('/Student/<string:user>', methods = ['POST', 'GET'])
def Student(user):
    error = None
    course = get_courses(user)
    return render_template('student.html', error = error, student_email = user, course = course)

@app.route('/display_personal_info/<string:email>/<string:login_type>', methods = ['POST', 'GET'])
def display_personal_info(email,login_type):
    error = None
    info = get_personal_info(email,login_type)
    return render_template('personal_info.html', error = error, info = info, login_type=login_type)

@app.route('/change_password/<string:email>/<string:login_type>', methods = ['POST', 'GET'])
def change_password(email, login_type):
    error = None
    if request.method == 'POST':
        #print('success')
        if request.form['newpass'] == request.form['confirmpass']:
            #print('success')
            error = update_password(login_type,email,request.form['oldpass'],request.form['newpass'])
        else:
            error = 'New Password and Confirm Password are not same! TRY AGAIN!'
        return render_template('change_password.html', error = error, email = email, login_type = login_type)

    #print('success')
    return render_template('change_password.html', error = error, email = email, login_type = login_type)

@app.route('/display_course/<string:email>/<string:course_id>/<float:section>', methods = ['POST', 'GET'])
def display_course(email,course_id,section):
    error = None
    course, prof_info, hw_description, hw_grades, exam_description, exam_grades  = get_course_info(email, course_id, section)
    if request.method == 'POST':
        if request.form['submit_button'] == 'drop_course':
            if drop_course(email,course_id):
                return redirect(url_for('Student', user = email))
            error = 'Unable To drop the course -> The Drop deadline has passed!'
        elif request.form['submit_button'] == 'post':
            return render_template('course_info.html', error = error, email = email, course = course, section = section, prof_info = prof_info, hw = hw_description, hw_grade = hw_grades, exam = exam_description, exam_grade = exam_grades)
    return render_template('course_info.html', error = error, email = email, course = course, section = section, prof_info = prof_info, hw = hw_description, hw_grade = hw_grades, exam = exam_description, exam_grade = exam_grades)

@app.route('/Professor/<string:user>', methods = ['POST', 'GET'])
def Professor(user):
    error = None
    course = teaching_course(user)
    return render_template('professor.html', error = error, email = user, course = course)

@app.route('/display_teaching/<string:email>/<string:course_id>/<float:section>', methods = ['POST', 'GET'])
def display_teaching(email, course_id, section):
    error = None
    course, hw, exam = get_teaching_info(email, course_id, section)
    print(course, hw, exam)
    if request.method == 'POST':
        #for adding a new post or comment
        return None
    
    return render_template('prof_teaching_course.html', error = error, email = email, course = course, section = section, hw = hw, exam = exam)

@app.route('/create_assignment/<string:email>/<string:assignment>', methods = ['POST', 'GET'])
def create_assignment(email, assignment):
    error = None
    return None

@app.route('/grade_course/<string:email>/<string:assignment>/<float:assignment_no>', methods = ['POST', 'GET'])
def grade_course(emai, assignment, assignment_no):
    error = None
    return render_template('assignment_grade.html', error = error)

@app.route('/Teaching Assistance/<string:user>', methods = ['POST', 'GET'])
def Teaching_assistance(user):
    error = None
    course = get_courses(user)
    return render_template('student.html', error = error, student_email = user, course = course)

def valid_credentials(login_type, email, password):
    conn = sqlite3.connect('Database/final_test.db')
    cursor = conn.execute("SELECT Password FROM "+str(login_type)+" WHERE EXISTS (SELECT Email FROM "+str(login_type)+" WHERE Email = '"+str(email)+"')")
    result = cursor.fetchall()
    for row in result:
        if row[0] == password:
            conn.close()
            return True
    conn.close()
    return False

def get_courses(email):
    conn = sqlite3.connect('Database/final_test.db')
    cursor = conn.execute("SELECT Course_id, Section_no FROM Enrolls WHERE Email = '" + str(email) + "'")
    result = cursor.fetchall()
    #for row in result:
        #print(row[0],row[1])
    conn.close()
    return result

def get_personal_info(email, login_type):
    conn = sqlite3.connect('Database/final_test.db')
    if login_type == 'Student':
        cursor = conn.execute("SELECT Email, Name, Age, Gender, Major, Street, Zipcode FROM Students WHERE Email = '"+str(email)+"'")
    else:
        cursor = conn.execute("SELECT Email, Name, Age, Gender, Office_address, Department, Title FROM Professors Where Email = '"+str(email)+"'")
    result = cursor.fetchall()
    conn.close()
    return result

def update_password(login_type, email, oldpass, newpass):
    if len(str(newpass)) <= 5:
        return 'New Password should be at least 6 characters'

    if(newpass == oldpass):
        return 'New Password Cannot be the same as old Password'

    if valid_credentials(login_type, email, oldpass):
        conn = sqlite3.connect('Database/final_test.db')
        #update password
        print(login_type, newpass, email)
        print("UPDATE "+str(login_type)+"s SET Password = '"+str(newpass)+"' WHERE Email = '"+str(email)+"'")
        conn.execute("UPDATE "+str(login_type)+"s SET Password = '"+str(newpass)+"' WHERE Email = '"+str(email)+"'")
        conn.close()

        #conn = sqlite3.connect('Database/final_test.db')
        #result = conn.execute("SELECT Password FROM Students WHERE Email = '"+str(email)+"'")
        #for row in result:
        #    print(row[0])
        #conn.close()
        return 'Successfuly Updates Password'

    return 'Old password does not match'

def get_course_info(email, course_id, section):
    conn = sqlite3.connect('Database/final_test.db')
    course = conn.execute("SELECT Course_id, Course_name, Course_description FROM Courses WHERE Course_id = '"+str(course_id)+"'")
    teaching_team_id = conn.execute("SELECT Teaching_team_id FROM Sections WHERE (Course_id = '"+str(course_id)+"' AND Sec_no = "+str(section)+")")
    for row in teaching_team_id:
        tid = row[0]
    prof_email = conn.execute("SELECT Email FROM Prof_teaching_teams WHERE Teaching_team_ID = "+str(tid)+"")
    for row in prof_email:
        pmail = row[0]
    prof_info = conn.execute("SELECT Name, Email, Office_address FROM Professors WHERE Email = '"+str(pmail)+"'")

    hw_grades = conn.execute("SELECT HW_no, Grade FROM Homework_grades WHERE (Email = '"+str(email)+"' AND Course_id = '"+str(course_id)+"' AND Sec_no = '"+str(section)+"')")
    hw_description = conn.execute("SELECT HW_no, HW_Details FROM Homeworks WHERE (Course_id = '"+str(course_id)+"' AND Sec_no = '"+str(section)+"')")

    exam_grades = conn.execute("SELECT Exam_no, Grade FROM Exam_grades WHERE (Email = '"+str(email)+"' AND Course_id = '"+str(course_id)+"' AND Sec_no = '"+str(section)+"')")
    exam_description = conn.execute("SELECT Exam_no, Exam_Details FROM Exams WHERE (Course_id = '"+str(course_id)+"' AND Sec_no = '"+str(section)+"')")

    c = course.fetchall()
    p = prof_info.fetchall()
    hw = hw_description.fetchall()
    hw_g = hw_grades.fetchall()
    ex = exam_description.fetchall()
    ex_g = exam_grades.fetchall()
    #post = conn.execute("SELECT post_no, post_info FROM Posts WHERE (student_email = '"+str(email)+"' AND course_id = '"+str(course_id)+"'")
    #comment = conn.execute("SELECT post_no, comment_no, comment_info FROM Comments WHERE (student_email = '"+str(email)+"' AND course_id = '"+str(course_id)+"'")
    
    #for row in course:
    #    print(row[0],row[1],row[2])

    conn.close()
    return c, p, hw, hw_g, ex, ex_g
    #, post, comment

def drop_course(email, course_id):
    conn = sqlite3.connect('Database/final_test.db')
    result = conn.execute("SELECT Late_drop_deadline FROM Courses WHERE Course_id = '"+str(course_id)+"'")
    r = result.fetchall()
    drop_date = str(r[0][0]).split('/')
    drop = datetime.date(2000+int(drop_date[2]),int(drop_date[0]),int(drop_date[1]))

    print(drop, datetime.date.today())

    if datetime.date.today() <= drop:
        conn.execute("DELETE FROM Enrolls WHERE (Email = '"+str(email)+"' AND Course_id = '"+str(course_id)+"')")
        #conn.execute("DELETE FROM Posts WHERE (Email = '"+str(email)+"' AND Course_id = '"+str(course_id)+"')")
        #conn.execute("DELETE FROM Comments WHERE (Email = '"+str(email)+"' AND Course_id = '"+str(course_id)+"')")
        return True
        #'Successfully Dropped the course '+str(course_id)

    return False
    #'Unsuccessfull to Drop the course '+str(course_id)+' (Course drop deadline has passed :'+str(drop)+' !!)'

def teaching_course(email):
    conn = sqlite3.connect('Database/final_test.db')
    teaching_id = conn.execute("SELECT Teaching_team_id FROM Prof_teaching_teams WHERE Email = '"+str(email)+"'")
    for row in teaching_id:
        tid = row[0]
    cursor = conn.execute("SELECT Course_id, Sec_no FROM Sections WHERE Teaching_team_id = '"+str(tid)+"'")
    result = cursor.fetchall()
    conn.close()
    return result

def get_teaching_info(email, course_id, section):
    conn = sqlite3.connect('Database/final_test.db')
    course = conn.execute("SELECT Course_id, Course_name, Course_description FROM Courses WHERE Course_id = '"+str(course_id)+"'")
    hw_description = conn.execute("SELECT HW_no, HW_Details FROM Homeworks WHERE (Course_id = '"+str(course_id)+"' AND Sec_no = '"+str(section)+"')")
    exam_description = conn.execute("SELECT Exam_no, Exam_Details FROM Exams WHERE (Course_id = '"+str(course_id)+"' AND Sec_no = '"+str(section)+"')")

    c = course.fetchall()
    h = hw_description.fetchall()
    e = exam_description.fetchall()
    conn.close()
    return c, h, e

#def create_post():
#def create_comment():

if __name__ == '__main__':
    app.run()