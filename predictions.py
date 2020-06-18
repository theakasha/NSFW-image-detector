import tflite_runtime.interpreter as tflite
from flask import request,redirect,url_for, jsonify, json,Flask,send_from_directory,render_template
import numpy as np
from PIL import Image
from io import BytesIO
import requests
import os
import boto3
import botocore
import zipfile


BUCKET_NAME = 'nsfw-inceptionv3'
MODEL_FILE_NAME ='converted_nsfw_model.tflite.zip'
MODEL_LOCAL_PATH=  MODEL_FILE_NAME

def download_model():
    s3=boto3.resource('s3')
    try:
        s3.Bucket(BUCKET_NAME).download_file(MODEL_FILE_NAME,MODEL_FILE_NAME)
        with zipfile.ZipFile(MODEL_FILE_NAME, 'r') as zip_ref:
            zip_ref.extractall(APP_ROOT)
        os.remove(MODEL_FILE_NAME)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The Object doesnot exist")
        else:
            raise


app=Flask(__name__)
APP_ROOT=os.path.dirname(os.path.abspath(__file__))

download_model()
interpreter = tflite.Interpreter(model_path="converted_nsfw_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_shape=input_details[0]['shape']


@app.route('/')
def index():
    return render_template("index.html")

#@app.route('/uploads/<filename>')
#def uploaded_file(filename):
#    return send_from_directory("static/images",
#                            filename)

@app.route("/upload",methods=['GET','POST'])
def upload():
    if request.method== 'POST' and 'file' in request.files:
        upload=request.files.getlist("file")[0]
        filename=upload.filename
    if request.method== 'GET':
        name=request.args.get('text')
        filename=name.rsplit('/',1)
        filename=filename[1]
        response=requests.get(name)
        upload=Image.open(BytesIO(response.content))
        

    if request.method=='POST' and 'file' not in request.files:
        name=request.form['text']
        filename=name.rsplit('/',1)
        filename=filename[1]
        response=requests.get(name)
        upload=Image.open(BytesIO(response.content))
        
        
    target=os.path.join(APP_ROOT, 'static/images/')

    #create image directory if not found
    if not os.path.isdir(target):
        os.mkdir(target)

    print("File name: {}".format(filename))
        
    ext=os.path.splitext(filename)[1]
    if(ext==".jpg")or (ext==".png") or(ext==".bmp") or (ext==".jpeg"):
        print("File accepted")
    else:
        filename+=".jpg"
        return("The file is not supported"),400

#     save file
    
    destination="/".join([target,filename])
    print("File saved to:", destination)
    upload.save(destination) 
    img=Image.open(destination)
    upload1 = img.resize((input_shape[1],input_shape[2]))
    im_array=np.array(upload1)
    im_array =im_array / 255
    x_test=np.array(im_array,dtype=np.float32)
    x_test = np.expand_dims(x_test, axis=0)
    interpreter.set_tensor(input_details[0]['index'], x_test)
    interpreter.invoke()
#    model_load()
#    load_model()
    pred = interpreter.get_tensor(output_details[0]['index'])
    dict={'Drawing':'0','Hentai':'0','Neutral':'0','Porn':'0','Sexy':'0'}
    dict['Drawing']=str.format(str(pred[0][0]))
    dict['Hentai']=str.format(str(pred[0][1]))
    dict['Neutral']=str.format(str(pred[0][2]))
    dict['Porn']=str.format(str(pred[0][3]))
    dict['Sexy']=str.format(str(pred[0][4]))
    os.remove(destination)
    return jsonify(dict), 200


if __name__ == '__main__':
    app.run()
