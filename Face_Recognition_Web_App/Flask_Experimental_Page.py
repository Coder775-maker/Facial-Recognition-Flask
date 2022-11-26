
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
#text = '<h3> Hello Web </h3>'
@app.route('/')
def home():
    return render_template('home_experimental.html')
################################################################################Spare Code Function
@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        #if file and allowed_file(file.filename):
        f.save(os.path.join("/home/anurag/Desktop/Face_Recognition_Flask/Unknown", f.filename))
        return render_template("home_experimental.html", filen = f.filename)

            #return render_template('unknown_error.html')
            # add return statement here!!!
@app.route("/delete", methods=['GET','POST'])
def delete_unknown():
    import os
    directory_name = "/home/anurag/Desktop/Face_Recognition_Flask/Unknown"
    testing = os.listdir(directory_name)

    for item in testing:
        if item.endswith(".jpg"):
            os.remove(os.path.join(directory_name, item))
    return render_template("home_experimental.html")

@app.route("/successk", methods=['POST'])
def successk():
    if request.method == 'POST':
        fk = request.files['filek']
    #if file and allowed_file(file.filename):
        fk.save(os.path.join("/home/anurag/Desktop/Face_Recognition_Flask/Known", fk.filename))
        return render_template("home_experimental.html", filenk = fk.filename)
        # add return statement here!!!

# Add Delte function here

@app.route("/deletek", methods=['GET','POST'])
def delete_known():
    import os
    directory_name = "/home/anurag/Desktop/Face_Recognition_Flask/Known"
    testing = os.listdir(directory_name)

    for itemk in testing:
        if itemk.endswith(".jpg"):
            os.remove(os.path.join(directory_name, itemk))
    return render_template("home_experimental.html")






################################################################################ Start of Face Recognition Function#

#@app.route("/delete", methods=['GET','POST'])
#def delete_unknown():
#    import os
#    directory_name = "/home/anurag/Desktop/Face_Recognition_Flask/Unknown"
#    testing = os.listdir(directory_name)

#    for item in testing:
#        if item.endswith(".jpg"):
#            os.remove(os.path.join(directory_name, item))
#    return render_template("home_experimental.html")

@app.route("/face_rec/", methods=['POST','GET'])
def face_recognise():

    import face_recognition
    import os
    import cv2
    import time
    z = 0
    known_faces_dir = "Known" # Filename
    unknown_faces_dir = "Unknown" # Filename
    tolerance = 0.54
    frame_thickness = 3
    font = 2
    Model = "cnn"

    print("loading known faces")
    known_faces = []
    known_names = []

    for name in os.listdir(known_faces_dir):
        print('printing dir name', name)
        #for filename in os.listdir(f"{known_faces_dir}/{name}"):
        image = face_recognition.load_image_file(f"{known_faces_dir}/{name}") # /{ filename} Only use if for loop above is uncommented
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(name)
    print('processing unknown images')
    for filename in os.listdir(unknown_faces_dir):
        print(filename)
        image = face_recognition.load_image_file(f"{unknown_faces_dir}/{filename}")
        locations = face_recognition.face_locations(image, model = Model)
        encodings = face_recognition.face_encodings(image, locations)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        for face_encoding, face_location in zip(encodings, locations):
            results = face_recognition.compare_faces(known_faces, face_encoding, tolerance)
            match = None
            if True in results:
                match = known_names[results.index(True)]
                print(f"Match found: {match}")
                MATCH = f"Match found: {match}" ########
                top_left = (face_location[3], face_location[0])
                bottom_right = (face_location[1], face_location[2])

                colour = [0,0,255]

                cv2.rectangle(image, top_left, bottom_right,colour,frame_thickness)

                top_left = (face_location[3], face_location[2])
                bottom_right = (face_location[1], face_location[2]+22)
                cv2.rectangle(image, top_left, bottom_right,colour,cv2.FILLED)
                cv2.putText(image, match, (face_location[3]+10, face_location[2]+15),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), font)
            cv2.imwrite('static/images/saved.png', image)
                #cv2.imwrite('/home/anurag/Desktop/Face_Recognition_Flask/static/images/saved.png', image)
            #elif False in results:
               # z = 1



        #cv2.imwrite('static/images/saved.png', image)
        #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'shovon.jpg')
        #cv2.imshow(filename, image)
        #cv2.waitKey(5000)
        #cv2.destroyWindow(filename)
        #if z == 1:
         #   return render_template('failed.html')

        return render_template('home_experimental.html', MATCH = MATCH, image_1 = "saved.png");




################################################################################End of Face REcognition Function VERY USEFUL ###return render_template('home.html', message2 = message2 );

if __name__ == '__main__':
    app.run(debug = True)
