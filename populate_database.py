import sqlite3
import pandas as pd
from sqlalchemy import Integer


data_s = pd.read_csv('cvs_files/Students_TA.csv')
data_p = pd.read_csv('cvs_files/Professors.csv')
data_c = pd.read_csv('cvs_files/Posts_Comments.csv')

conn = sqlite3.connect('Database/final_test.db')

#Students
students = data_s[['Full Name', 'Age', 'Gender', 'Major', 'Street', 'Zip', 'Email', 'Password']]
student = students.rename(columns={'Full Name':'Name', 'Zip':'Zipcode'})
student.to_sql('Students', conn, if_exists = 'replace', index = False)

#Zipcodes
zipcode = data_s[['Zip', 'City', 'State']]
z = zipcode.rename(columns={'Zip':'Zipcode'})
z.to_sql('Zipcodes', conn, if_exists = 'replace', index = False)

#Professors
professors = data_p[['Name', 'Email', 'Password', 'Age', 'Gender', 'Office', 'Department', 'Title']]
prof = professors.rename(columns={'Office':'Office_address'})
prof.to_sql('Professors', conn, if_exists = 'replace', index = False)

#Departments
departments = data_p.loc[data_p['Title'] == 'Head',['Department', 'Department Name','Name']]
dept = departments.rename(columns={'Department':'Dept_id', 'Department Name':'Dept_name', 'Name':'Dept_head'})
dept.to_sql('Departments', conn, if_exists = 'replace', index = False)

#Courses
course = data_c[['Courses', 'Drop Deadline']]
courses = course.rename(columns={'Courses':'Course_id', 'Drop Deadline':'Late_drop_deadline'})
c_1 = data_s[['Courses 1', 'Course 1 Name', 'Course 1 Details']]
c_2 = data_s[['Courses 2', 'Course 2 Name', 'Course 2 Details']]
c_3 = data_s[['Courses 3', 'Course 3 Name', 'Course 3 Details']]
course_details = pd.concat([c_1.rename(columns={'Courses 1':'Course_id','Course 1 Name':'Course_name','Course 1 Details':'Course_description'}),c_2.rename(columns={'Courses 2':'Course_id','Course 2 Name':'Course_name','Course 2 Details':'Course_description'}),c_3.rename(columns={'Courses 3':'Course_id','Course 3 Name':'Course_name','Course 3 Details':'Course_description'})])
new_course = course_details.drop_duplicates(ignore_index = True)
final_course = pd.merge(left = courses, right = new_course,left_on = 'Course_id', right_on = 'Course_id' , sort = True)
final_course.to_sql('Courses', conn, if_exists = 'replace', index = False)

#Sections
sections_courseID = data_p[['Teaching', 'Teaching Team ID']]
sec_courseID = sections_courseID.rename(columns={'Teaching':'Course_id'})
section_numberlimit_1 = data_s[['Courses 1', 'Course 1 Section', 'Course 1 Section Limit']]
section_numberlimit_2 = data_s[['Courses 2', 'Course 2 Section', 'Course 2 Section Limit']]
section_numberlimit_3 = data_s[['Courses 3', 'Course 3 Section', 'Course 3 Section Limit']]
a = section_numberlimit_1.rename(columns={'Courses 1': 'Course_id', 'Course 1 Section': 'Sec_no', 'Course 1 Section Limit': 'Limit'})
b = section_numberlimit_2.rename(columns={'Courses 2': 'Course_id', 'Course 2 Section': 'Sec_no', 'Course 2 Section Limit': 'Limit'})
c = section_numberlimit_3.rename(columns={'Courses 3': 'Course_id', 'Course 3 Section': 'Sec_no', 'Course 3 Section Limit': 'Limit'})
section = pd.concat([a,b,c])
new_section = section.drop_duplicates(ignore_index = True)

final_section = pd.merge(left=new_section,right=sec_courseID,left_on='Course_id',right_on='Course_id',sort=True)
final_section.to_sql('Sections', conn, if_exists = 'replace', index = False)

#Enrolls
enroll_1 = data_s[['Email', 'Courses 1', 'Course 1 Section']]
enroll_2 = data_s[['Email', 'Courses 2', 'Course 2 Section']]
enroll_3 = data_s[['Email', 'Courses 3', 'Course 3 Section']]
enroll = pd.concat([enroll_1.rename(columns = {'Courses 1': 'Course_id', 'Course 1 Section': 'Section_no'}), enroll_2.rename(columns= {'Courses 2': 'Course_id', 'Course 2 Section': 'Section_no'}), enroll_3.rename(columns = {'Courses 3': 'Course_id', 'Course 3 Section': 'Section_no'})])

enroll.to_sql('Enrolls', conn, if_exists = 'replace', index = False)

#Prof_Teaching_Teams
prof_teaching_team = data_p[['Email', 'Teaching Team ID']]
prof_teach_team = prof_teaching_team.rename(columns={'Teaching Team ID':'Teaching_team_id'})
prof_teach_team.to_sql('Prof_teaching_teams', conn, if_exists = 'replace', index = False)

#TA_Teaching_Teams
ta_teaching_team = data_s[['Email', 'Teaching Team ID']]
new_ta_teaching_team = ta_teaching_team.dropna(axis = 0, subset = ['Teaching Team ID'])
ta_teach_team = new_ta_teaching_team.rename(columns={'Teaching Team ID':'Teaching_team_id'})
ta_teach_team.to_sql('TA_teaching_teams', conn, if_exists = 'replace', index = False)

#hw
hw_1 = data_s[['Courses 1','Course 1 Section','Course 1 HW_No','Course 1 HW_Details']]
hw_2 = data_s[['Courses 2','Course 2 Section','Course 2 HW_No','Course 2 HW_Details']]
hw_3 = data_s[['Courses 3','Course 3 Section','Course 3 HW_No','Course 3 HW_Details']]

hw = pd.concat([hw_1.rename(columns={'Courses 1':'Course_id','Course 1 Section':'Sec_no','Course 1 HW_No':'HW_no','Course 1 HW_Details':'HW_Details'}),hw_2.rename(columns={'Courses 2':'Course_id','Course 2 Section':'Sec_no','Course 2 HW_No':'HW_no','Course 2 HW_Details':'HW_Details'}),hw_3.rename(columns={'Courses 3':'Course_id','Course 3 Section':'Sec_no','Course 3 HW_No':'HW_no','Course 3 HW_Details':'HW_Details'})]).drop_duplicates(ignore_index = True).sort_values(by = 'Course_id')
hw.to_sql('Homeworks', conn, if_exists = 'replace', index = False)

#hw grades


#exam


#exam grades


#posts
post = data_c[['Courses','Post 1','Post 1 By']]


#comments
