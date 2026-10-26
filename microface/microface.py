import face_recognition
import mysql.connector
import os
import time
import json
import requests
import cv2
import csv
import PIL
from PIL import Image  
from datetime import date
from six.moves import cPickle as pickle
from django.db import connection
from io import BytesIO

def teachFace(picture, emp_code):
	t = time.localtime()
	current_time = time.strftime("%H:%M:%S", t)
	print("start time")
	print(current_time)
	facefile = 'known_faces/'+emp_code

	name_image = face_recognition.load_image_file(picture)
	face_locations = face_recognition.face_locations(name_image,number_of_times_to_upsample=0, model="hog")
	faces = face_recognition.face_encodings(name_image,known_face_locations=face_locations,num_jitters=0)
	if len(faces) > 1 :
		saveFailureResponse('teachFace','2','Too Many Faces !',picture)
		return(2,'Too Many Faces !')
	elif len(faces) == 0:
		saveFailureResponse('teachFace','2','No Face Found !',picture)
		return(2,'No Face Found !')
	else:
		exists = os.path.isfile(facefile)
		if exists:
			fileobj = open(facefile,'rb')
			facelist = pickle.load(fileobj)
			fileobj.close()
			faces = faces + facelist
			teachFaceModelToDb(emp_code, facefile)

		fileobj = open(facefile,'wb')
		pickle.dump(faces,fileobj)
		fileobj.close()
		# Insert into DB if newly face model created at known-faces
		t = time.localtime()
		current_time = time.strftime("%H:%M:%S", t)
		print("end time")
		print(current_time)
		return(0,'Learnt !')	

def findFace(picture):
	t = time.localtime()
	current_time = time.strftime("%H:%M:%S", t)
	print("start time")
	print(current_time)
	image = Image.open(picture)
	# print(image)
	friend_path = 'known_faces/'
	# print('find face test')
	name_image = face_recognition.load_image_file(picture)
	#face_locations = face_recognition.face_locations(name_image,number_of_times_to_upsample=0, model="cnn")
	face_locations = face_recognition.face_locations(name_image,number_of_times_to_upsample=1,model="hog")
	#print(len(face_locations)
	if len(face_locations) == 0:
		saveFailureResponse('findFace','2','No Face Found !',picture)
		return (2,'No Face Found !')
	elif len(face_locations) > 1 :
		saveFailureResponse('findFace','2','Too Many Faces !',picture)
		return(2,'Too Many Faces !')

	t = time.localtime()
	current_time = time.strftime("%H:%M:%S", t)
	print("face locations done time")
	print(current_time)
	# face_locations = face_recognition.face_locations(name_image)
	faces = face_recognition.face_encodings(name_image,known_face_locations=face_locations ,num_jitters=70, model="large")
	
	t = time.localtime()
	current_time = time.strftime("%H:%M:%S", t)
	print("face encodings done time")
	print(current_time)
	# faces = face_recognition.face_encodings(name_image)
	
	matched = []
	accuracy = 0
	known_faces = [f for f in os.listdir(friend_path) if os.path.isfile(friend_path + f)]
	for i in known_faces:
		fileobj = open(friend_path+i,'rb')
		print(">>>> Detection comparing with model == ",fileobj)
		face_list = pickle.load(fileobj)
		for j in faces:
			result = face_recognition.compare_faces(face_list, j, tolerance=0.35)
			if result[0]:
				print("accuracy")
				# print(accuracy_score(result[0], j))
				matched.append(i)
				print(matched)
				break
	t = time.localtime()
	current_time = time.strftime("%H:%M:%S", t)
	print("end time")
	print(current_time)
	if len(matched) == 0:
		saveFailureResponse('findFace','1','No Match !',picture)
		return(1,'No Match !')
	elif len(matched) > 1:
		saveFailureResponse('findFace','2','Multiple Faces Matched!  Faces:'+', '.join(matched),picture)
		return(2,'Multiple Faces Matched!  Faces:'+', '.join(matched))
	#saveFailureResponse('findFace','0','User Image to be Processed',picture)
	return(0,', '.join(matched))

def newFace(picture, emp_code):
	t = time.localtime()
	current_time = time.strftime("%H:%M:%S", t)
	print("start time")
	print(current_time)
	facefile = 'known_faces/'+emp_code
	name_image = face_recognition.load_image_file(picture) #file path when API calling POST API, INTO numpy array
	face_locations = face_recognition.face_locations(name_image,number_of_times_to_upsample=0, model="hog") #rect box around face,returns A list of tuples of found face locations
	faces = face_recognition.face_encodings(name_image,known_face_locations=face_locations,num_jitters=0)#For given image, returns the 128-dimension face encoding for each face in the image.

	if len(faces) > 1 :
		saveFailureResponse('newFace','2','Too Many Faces !',picture)
		return(2,'Too Many Faces !')
	elif len(faces) == 0:
		saveFailureResponse('newFace','2','No Face Found !',picture)
		return(2,'No Face Found !')
	else:
		# fileobj = open(facefile,'wb')
		# pickle.dump(faces,fileobj)
		# fileobj.close()
		# if(UserExistsAtDb(name, DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT)):
		if(UserExistsAtDb(emp_code)):
			if (deleteFace(emp_code)[0] == 0):
				fileobj = open(facefile,'wb')
				pickle.dump(faces,fileobj)
				fileobj.close()
				# If employee code exists at DB, delete it first from both folder and DB, again insertintoDB
				db_inserted = insertBlobToDb(emp_code,facefile)
				if(db_inserted):
					t = time.localtime()
					current_time = time.strftime("%H:%M:%S", t)
					print("end time")
					print(current_time)
					return(0,'Deleted and New Face Added')

				return(0,"Employee Code exists at DB")
			else:
				return (0, "Employee ID exist in DB but Face_Model not present")
		else : 
			fileobj = open(facefile,'wb')
			pickle.dump(faces,fileobj)
			fileobj.close()
			db_inserted = insertBlobToDb(emp_code,facefile)
			if(db_inserted):
				t = time.localtime()
				current_time = time.strftime("%H:%M:%S", t)
				print("end time")
				print(current_time)
				return(0,'New Face Added !')

def listOfUsers():
	friend_path = 'known_faces/'
	known_faces = [f for f in os.listdir(friend_path) if os.path.isfile(friend_path + f)]
	return(2,known_faces)

def deleteFace(emp_code):
	file_path = 'known_faces/'+emp_code
	# checking whether file exists or not
	if os.path.exists(file_path):
		# removing the file using the os.remove() method
		os.remove(file_path)
		#NOTE: DELETING FILE FROM Known_faces DATABASE TABLE 
		with connection.cursor() as cursor:
			# NOTE: DELETE statement does not return any data. so, cursur.fetchall() func not work here
			# Deleting on the basis of employee code
			result = cursor.execute("DELETE FROM known_faces WHERE emp_code=%s", (emp_code,))
			# cursor.fetchall()
			if result > 0:
				print("File deleted successfully")
				return (0, 'File deleted successfully')
			else:
				return (1, 'Face-model not deleted')
		# return(0,'File Deleted Successfully')
	else:
		print("Face-Model not found")
		return(2,'No such File Found')

def saveImage(image,imageName):
	img = Image.open(image)
	# Path where image is saved
	path = 'Logs/'
	img.save(path+str(imageName),format="JPEG")

def saveFailureResponse(api_name, ret_code, msg, image = ''):
	# Get current Date
	today = date.today()
	current_date = today.strftime("%d %m %Y")
	
	# File to be Logged
	filename = 'Logs/'+current_date+'.csv'
	
	#csv Header Fields
	fields = ["Date [time]", "Api Name", "Return Code", "Response Message", "Image Name"]

	lt = time.localtime()
	current_time = time.strftime("%H:%M:%S", lt)
	print(current_time)

	#===========================================================================================================================
	# NOTE : 	Saving Image file for these cases : ['No Face Found', 'Too Many Faces', 'No Match', 'Multiple Face Matched', ] 
	# 			also ret_code is not 0, and getting image in this case
	#===========================================================================================================================
	
	if(ret_code != 0 and image != ''):
		# Get current Time in millis
		millis = int(round(time.time() * 1000))
		saveImage(image,millis)

		# data rows of csv file in case of not recognized well
		rows = [str(today)+'['+str(current_time)+']',str(api_name), str(ret_code), str(msg), str(millis)+'.jpeg']
		
		if not os.path.exists(filename):
			with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
				# creating a csv writer object for header
				writer = csv.DictWriter(csvfile, fieldnames=fields)
				writer.writeheader()
				
				# creating a csv writer object for rows
				csvwriter = csv.writer(csvfile)
			
				# writing the data rows 
				csvwriter.writerow(rows)
		else:
			with open(filename, 'a+', newline='', encoding='utf-8') as csvfile:
				# creating a csv writer object 
				csvwriter = csv.writer(csvfile) 
			
				# writing the data rows 
				csvwriter.writerow(rows)

	else:
		# data rows of csv file 
		rows = [str(today)+'['+str(current_time)+']',str(api_name), str(ret_code), str(msg), 'NULL']
		
		if not os.path.exists(filename):
			with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
				# creating a csv writer object for header
				writer = csv.DictWriter(csvfile, fieldnames=fields)
				writer.writeheader()
				
				# creating a csv writer object for rows
				csvwriter = csv.writer(csvfile)
			
				# writing the data rows 
				csvwriter.writerow(rows)
		else:
			with open(filename, 'a+', newline='', encoding='utf-8') as csvfile:
				# creating a csv writer object 
				csvwriter = csv.writer(csvfile) 
			
				# writing the data rows 
				csvwriter.writerow(rows)

def saveNodeLog(api_name, emp_id, request_obj, response_obj = '', error = ''):
	# Get current Date
	today = date.today()
	current_date = today.strftime("%d %m %Y")

	# Get current Time in millis
	millis = int(round(time.time() * 1000))

	# File to be Logged
	filename = 'Logs/success_'+current_date+'.csv'
	
	#csv Header Fields
	fields = ["Date [time]","Api Name","Employee_ID", "Request Body", "Response Body", "Error"] 	
	t = time.localtime()
	current_time = time.strftime("%H:%M:%S", t)
	print(current_time)
	# data rows of csv file 
	# rows = [str(today)+'['+str(current_time)+']', str(api_name),str(emp_id), "Node Api Call Failed", "2002",str(error)]
	if(error == ''):
		rows = [str(today)+'['+str(current_time)+']', str(api_name),str(emp_id), str(request_obj), str(response_obj), 'NULL']
		if not os.path.exists(filename):
			with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
				# creating a csv writer object for header
				writer = csv.DictWriter(csvfile, fieldnames=fields)
				writer.writeheader()
				
				# creating a csv writer object for rows
				csvwriter = csv.writer(csvfile)
			
				# writing the data rows 
				csvwriter.writerow(rows)
				
		else:
			with open(filename, 'a+', newline='', encoding='utf-8') as csvfile:
				# creating a csv writer object 
				csvwriter = csv.writer(csvfile) 
			
				# writing the data rows 
				csvwriter.writerow(rows)

	else:
		#If any Internal Server Error 500 occured
		rows = [str(today)+'['+str(current_time)+']', str(api_name),str(emp_id), str(request_obj),'NULL', str(error)]
		if not os.path.exists(filename):
			with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
				# creating a csv writer object for header
				writer = csv.DictWriter(csvfile, fieldnames=fields)
				writer.writeheader()
				
				# creating a csv writer object for rows
				csvwriter = csv.writer(csvfile)
			
				# writing the data rows 
				csvwriter.writerow(rows)
				
		else:
			with open(filename, 'a+', newline='', encoding='utf-8') as csvfile:
				# creating a csv writer object 
				csvwriter = csv.writer(csvfile) 
			
				# writing the data rows 
				csvwriter.writerow(rows)

def faceModelToBinaryData(face_model):
	with open(face_model, 'rb') as file:
		binaryData = file.read()
	return binaryData

def UserExistsAtDb(emp_code):
	with connection.cursor() as cursor:
		result = cursor.execute("SELECT id FROM known_faces WHERE emp_code=%s", (emp_code,))
		userRecord = cursor.fetchall()
		if(len(userRecord) == 0):
			return False
		else:
			print("Employee Id already exists")
			return True

#NOTE: Changes for handling the exception in insertion of model in DB 
def insertBlobToDb(emp_code, face_model):
	with connection.cursor() as cursor:
		emp_picture = faceModelToBinaryData(face_model)
		try:
			result = cursor.execute("INSERT INTO known_faces (emp_code, face_model) VALUES ( %s, %s)", (emp_code, emp_picture))
			print("Inserted Model sucessfully to DB")
			return True
		except Exception as e:
			print("Error while inserting face-model to DB, error : ", e)
			return False

def uploadAllModelToDb():
	known_faces_path = 'known_faces/'
	for f in os.listdir(known_faces_path):
		if os.path.isfile(known_faces_path+f):
			print("For user: ", f)
			insertBlobToDb(name=f, face_model=known_faces_path+f)

def storeFaceModelToKnownFaces(data, filename):
	with open(filename, 'wb') as file:
		# print("started writing data")
		file.write(data)

def fetchFaceModel():
	print("Fetching all user face-model data from DB")
	try:
		with connection.cursor() as cursor:
			cursor.execute("SELECT emp_code, face_model from known_faces")
			record = cursor.fetchall()
			# print(record)
			location = os.getcwd()+"/known_faces/" #Please change the PATH as defined in server
			for row in record:
				emp_code = row[0]
				face_model = row[1]
				print("Storing employee image on known_faces \n")
				storeFaceModelToKnownFaces(face_model, location+emp_code)
	except Exception as e:
		print("Failed to fetch user face-model, Reason: ",e)
	finally:
		cursor.close()
		print("MySQL connection is closed")

def getEmployeeDetails(node_get_employee_details, emp_id):
	response = requests.get(url=node_get_employee_details+emp_id,timeout=30)
	if response != None and response != "":
		response_body_unicode = response.content.decode('utf-8')
		response_body = json.loads(response_body_unicode)
		return response_body

#NOTE: Changes for handling the exception in insertion of model in DB 
def teachFaceModelToDb(emp_code, face_model):
	with connection.cursor() as cursor:
		result = cursor.execute("SELECT id, emp_code FROM known_faces WHERE emp_code=%s", (emp_code,))
		userRecord = cursor.fetchall()
		print(">>>> userRecord ==", userRecord)
		faceModelToUpdate = faceModelToBinaryData(face_model)
		try:
			updateResult = cursor.execute("UPDATE known_faces SET face_model=(%s) where id=(%s)", (faceModelToUpdate,userRecord[0][0]))
			print("updated table with latest face-model")
			return True
		except Exception as e:
			print("Error while updating face-model at teach API , error : ", e)
			return False
		
#FOR CRONJOB
def findStatusAndDelete(get_employee_details):
    known_faces_path = 'known_faces/'
    known_faces_array = [f for f in os.listdir(known_faces_path) if os.path.isfile(known_faces_path + f)]
    with connection.cursor() as cursor:
        result = cursor.execute("SELECT emp_code FROM known_faces")
        fetch_rows_array = []
        for fetch_emp_code_row in cursor.fetchall():
            fetch_rows_array.append(fetch_emp_code_row[0])

        for indi_emp_code in fetch_rows_array:
            get_current_status = getEmployeeDetails(get_employee_details, emp_id= indi_emp_code)
            if get_current_status['status_code'] == "1003" or get_current_status['status_code'] == "1004":
                for non_splited_name in known_faces_array:
                    if non_splited_name == indi_emp_code:
                        os.remove(known_faces_path + non_splited_name)
                        print("Removed form known_face_folder")
                    else:
                        print("Facing Error in deleting from folder")
                
                result = cursor.execute("DELETE FROM known_faces WHERE emp_code=%s", (indi_emp_code, ))
                if result > 0:
                    print("Deleted From DB")
                else:
                    print("Error from Deletion From DB")