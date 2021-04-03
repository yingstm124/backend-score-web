# from pymysql import cursors
# from segmentation import Segmentation
# from pre_processing import Pre_Processing
# from utility import showImage
from flask import Flask, flash, request, redirect, jsonify, render_template, send_from_directory
from flask.helpers import flash
from flask_cors import CORS
import pymysql
# import os
# import cv2
# import json
# from predict import Predict
# from PIL import Image

import numpy as np


# upload file image
UPLOAD_FOLDER = '/Users/sutimarpengpinij/Desktop/204361_OOD/backend/image'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


app = Flask(__name__, static_folder='image')
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGE_UPLOADS'] = '/Users/sutimarpengpinij/Desktop/204361_OOD/backend/image'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# cursor = db.cursor()
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})



# cors = CORS(app) http://localhost:56107

def connect_db():
    return pymysql.connect(

        user = 'b13246bc87d829',
        host = 'us-cdbr-east-03.cleardb.com', 
        password = 'e98c008b', 
        database = 'heroku_40db6ab2e8a1ba1', 
        autocommit = True, 
        charset = 'utf8mb4', 
        cursorclass = pymysql.cursors.DictCursor
    )

def get_db():
    '''Opens a new database connection per request.'''        
    if not hasattr(app, 'db'):
        app.db = connect_db()
    return app.db    



@app.route('/')
def home():
    return 'My back-end'


# ---------- User ---------------------
@app.route('/api/getUser/<email>', methods=['GET'])
def getUser(email):

    if request.method == 'GET':
        
        cursor = get_db().cursor()
        try:
            sql = "SELECT * FROM user WHERE email=%s"
            cursor.execute(sql, email)
            result = cursor.fetchone()

            print("result",result)

        except pymysql.OperationalError as e:
            print(e.args[0])
        
        # finally:
        #     cursor.close()

        # if(result != None):
        #     return convert_2_JSON(result, cursor) 

    return jsonify(result)


@app.route('/api/login', methods=['GET','POST'])
def login():

    email = request.json['email']
    password = request.json['password']

    print(email)
    print(password)

    cursor = get_db().cursor()

    try:
        sql = "SELECT * FROM user WHERE email=%s"
        cursor.execute(sql, email)
        result = cursor.fetchone()
        print(result)

        if(result != None):
            if result['password'] == password:
                status = 'pass'
            else:
                status = 'password incorrect'
    
        else:
            status = 'not found user'

    except pymysql.OperationalError as e:
        print(e.args[0])

    # finally: 
    #     cursor.close()

    return jsonify(result)


@app.route('/api/register', methods=['POST'])
def register():

    if request.method == 'POST':

        print('add user')
        print(request.json)
        content = request.json
        email = content['email']
        username = content['username']
        password = content['password']
        firstname = content['firstname']
        lastname = content['lastname']

        print(email)
        print(username)
        print(password)
        print(firstname, " ",lastname)

        cursor = get_db().cursor()
    
        try:
            sql = "INSERT INTO `user`(`email`, `userName`, `password`, `fname`, `lname`) VALUES (%s,%s,%s,%s,%s)"  
            cursor.execute(sql, (email, username, password, firstname, lastname))
            # db.commit()
            status = True 

        except pymysql.Error as e:
            print(e.args[0],e.args[1])
            status = False

        # finally:
        #     cursor.close()    
    
    return jsonify(status)


# --------------- Course

@app.route('/api/getCourse/<email>', methods=['GET'])
def getCourses(email):
    print('get Course ',email)

    if request.method == 'GET':
        
        cursor = get_db().cursor()

        try:
            sql = "SELECT c.courseId, c.courseName, c.exNo, s.term, s.year FROM course c INNER JOIN semester s ON c.semNo = s.semId WHERE c.teacheremail = %s"
            cursor.execute(sql,email)
            result = cursor.fetchall()

            if(result != None):
                print(result)
        
        except pymysql.OperationalError as e:
            print(e.args[0])

        # finally:
        #     cursor.close()
   
    return jsonify(result) 

# ---------- ExamType

@app.route('/api/getExams/<examId>', methods=['GET'])
def getExams(examId):
    print('get Course of ',examId)

    if request.method == 'GET':
        cursor = get_db().cursor()

        try:
            sql = "SELECT et.id, et.name, et.score, et.description FROM exam e INNER JOIN examType et ON e.examId = et.id WHERE e.examId = %s"
            cursor.execute(sql, examId)
            result = cursor.fetchall()

            if(result != None):
                # json_data = convert_2_JSON_list(result, cursor)
                print(result)

        except pymysql.OperationalError as e:
            print(e.args[0])

        # finally:
        #     cursor.close()
    
    return jsonify(result)

@app.route('/api/getExamType/<examId>/<name>', methods=['GET'])
def getExamType(examId, name):

    print(examId, name)

    if request.method == 'GET':
        
        cursor = get_db().cursor()
        try:
            sql = "SELECT id, name, score, description FROM examType WHERE id=%s AND name=%s"
            cursor.execute(sql, (examId, name))
            result = cursor.fetchone()

            print("result",result)

        except pymysql.OperationalError as e:
            print(e.args[0])


    return jsonify(result)


@app.route('/api/addExamType', methods=['POST'])
def addExamType():
    print('add Exam type of ')

    if request.method == 'POST':
        
        contents = request.json
        id = contents['id']
        name = contents['name']
        score = contents['score']
        description = contents['description']

        cursor = get_db().cursor()
        
        try: 
            sql = "INSERT INTO examType (id, name, score, description) VALUES (%s,%s,%s,%s)"
            cursor.execute(sql, (id, name, score, description))
            # db.commit()
            status = True 

        except pymysql.Error as e:
            print(e.args[0],e.args[1])
            status = False

        # finally:
        #     cursor.close()

    return jsonify(status)

@app.route('/api/editExamType/<id>', methods=['PUT'])
def editExamType(id):
    print('edit Exam Type ',id)

    if request.method == 'PUT':
        contents = request.json

        name = contents['name']
        score = contents['score']

        cursor = get_db().cursor()
        
        try: 
            sql = "UPDATE examType SET score=%s WHERE id=%s AND name=%s"
            cursor.execute(sql, (score,id,name))
            # db.commit()
            status = True 

        except pymysql.Error as e:
            print(e.args[0],e.args[1])
            status = False

    return jsonify(status)


@app.route('/api/getExamDetail/<name>/<id>', methods=['GET'])
def getExamScore(name,id):
    print('get Exam Score ',name,id)

    if request.method == 'GET':
        cursor = get_db().cursor()

        try:
            sql = "SELECT s.stdId, s.fname, s.lname, es.score, es.statusScan, es.examTypeNo, es.image FROM examScore es INNER JOIN student s ON s.stdId = es.stdNum WHERE es.examName = %s AND es.examTypeNo = %s"
            cursor.execute(sql, (name,id))
            result = cursor.fetchall()

            print(result)

            if(result != None):
                # json_data = convert_2_JSON_list(result, cursor)
                print(result)

        except pymysql.OperationalError as e:
            print(e.args[0])

        # finally:
        #     cursor.close()
    
    return jsonify(result)

@app.route('/api/addExamScore', methods=['POST'])
def addExamScore():
    print('add Exam Score ')

    if request.method == 'POST':

        contents = request.json
        print(contents)
        status = False
        for c in contents:
            examName = c['examName']
            examTypeNo = c['examTypeNo']
            stdNum = c['stdNum']
            score = c['score']

            cursor = get_db().cursor()
            try:
                sql = "INSERT INTO `examScore` (`examTypeNo`, `examName`,`stdNum`, `score`) VALUES (%s,%s,%s,%s)"  
                cursor.execute(sql, (examTypeNo, examName, stdNum, score))
                # db.commit()
                status = True 

            except pymysql.Error as e:
                print(e.args[0],e.args[1])
                status = False

            # finally:
            #     cursor.close()

    return jsonify(status)

@app.route('/api/editExamScoreStatus/<id>/<name>/<stdId>', methods=['PUT'])
def editExamScoreStatus(id, name, stdId):
    print('edit Exam Score Status')

    if request.method == 'PUT':

        contents = request.json
        statusScan = contents['statusScan']

        cursor = get_db().cursor()

        try:
            sql = "UPDATE examScore SET statusScan=%s WHERE examTypeNo=%s AND examName=%s AND stdNum=%s"
            cursor.execute(sql, (statusScan,id,name,stdId))
            status = True
        
        except pymysql.Error as e:
            print(e.args[0],e.args[1])
            status = False
    
    return jsonify(status)

@app.route('/api/editExamScore/<id>/<name>/<stdId>', methods=['PUT'])
def editExamScore(id, name, stdId):
    print('edit ExamScore',id, name, stdId)

    if request.method == 'PUT':

        contents = request.json
        score = contents['score']

        cursor = get_db().cursor()
        
        try: 
            sql = "UPDATE examScore SET score=%s WHERE examTypeNo=%s AND examName=%s AND stdNum=%s"
            cursor.execute(sql, (score,id,name,stdId))
            # db.commit()
            status = True 

        except pymysql.Error as e:
            print(e.args[0],e.args[1])
            status = False

    return jsonify(status)

@app.route('/api/delExamType/<id>/<name>', methods=['POST'])
def delExamType(id,name):
    print('del ExamType', id,name)

    if request.method == 'POST':

        cursor = get_db().cursor()
        try:
            sql = "DELETE FROM examType WHERE id=%s AND name=%s"
            cursor.execute(sql, (id,name))
            # db.commit()
            status = True

        except pymysql.Error as e:
            print(e.args[0],e.args[1])
            status = False

        # finally:
        #     cursor.close()

        return jsonify(status)



# ---------- Register Student

@app.route('/api/getRegStudents/<courseId>', methods=['GET'])
def getRegStudent(courseId):
    print('get register student', courseId)

    if request.method == 'GET':
        cursor = get_db().cursor()

        try:
            sql = "SELECT rs.stdNo, s.fname, s.lname FROM register rs INNER JOIN student s ON rs.stdNo = s.stdId WHERE rs.cNo = %s"
            cursor.execute(sql, (courseId))
            result = cursor.fetchall()

            if(result != None):
                # json_data = convert_2_JSON_list(result, cursor)
                print(result)

        except pymysql.OperationalError as e:
            print(e.args[0])

        # finally:
        #     cursor.close()
    
    return jsonify(result)

@app.route('/api/getStudent/<examId>',methods=['GET'])
def getStudent(examId):
    print('get student ',examId)

    if request.method == 'GET':
        cursor = get_db().cursor()

        try:
            sql = "SELECT s.fname, s.lname, rs.stdNo FROM exam e INNER JOIN course c ON e.examId = c.exNo INNER JOIN register rs ON rs.cno = c.courseId INNER JOIN student s ON s.stdId = rs.stdNo WHERE e.examId = %s"
            cursor.execute(sql, examId)
            result = cursor.fetchall()

            if(result != None):
                # json_data = convert_2_JSON_list(result, cursor)
                print(result)

        except pymysql.OperationalError as e:
            print(e.args[0])

        # finally:
        #     cursor.close()
    
    return jsonify(result)


# --- Image
@app.route('/api/getImage/<image_name>')
def getImageLink(image_name):

    return send_from_directory(app.config['IMAGE_UPLOADS'], filename=image_name)

@app.route('/api/uploadeImage/<examId>/<examName>/<studentId>', methods=['POST'])
def uploadImage(examId, examName, studentId):
    
    if request.method == 'POST':

        contents = request.json
        file = contents['file']
        print('file ==> ',file)

        cursor = get_db().cursor()

        try:
            sql = "UPDATE examScore SET image=%s WHERE examName=%s AND examTypeNo=%s AND stdNum=%s"
            cursor.execute(sql,(file, examName, examId, studentId))
            status = True
        except pymysql.Error as e:
            print(e.args[0],e.args[1])
            status = False

    return jsonify(status)


@app.route('/api/uploadfile/<filename>', methods=['POST'])
def upload_file(filename):

    status = False

    if request.method == 'POST':

        print(request.files['photo'])

        f = request.files['photo']

        if f.filename != '':
            path = './image/' + f.filename
            f.save(path)


        else:
            print('not found')
            
        print('end')

    return jsonify(status)


# --- Predict

@app.route('/api/predict/<img_path>', methods=['GET','POST'])
def predict(img_path):

    print('predict')

    # path = './image/' + img_path
    # img = cv2.imread(path)
    # binary_image = Pre_Processing(img).getBinaryImage()
    # digit_list, score_box = Segmentation(binary_image).getID_ScoreBox()

    # # student ID
    # result_std = ''
    # count = len(digit_list)
    # for d in digit_list:
    #     result = str(Predict(d).getResult())
    #     result_std += result

    # print('result student id ', result_std)

    # # score
    # count = len(score_box)
    # result_score = ''

    # if(count != 0):
    #     for s in score_box:
    #         result = str(Predict(s,True).getResult())
    #         result_score += result
    #         count -= 1
    # else: 
    #     result = 0

    # result_score = int(result_score)
    # print('result score ',result_score)

    result_std = '390513127'
    result_score = 6


    return jsonify({'result_std':result_std, 'result_score':result_score})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    