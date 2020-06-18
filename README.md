# NSFW-detector
It is a Not Safe For Work Detector web application
It's deployed using flask,tensorflow lite on aws lambda using zappa framework.
The model is an Inception-v3 model which is trained using transfer learning with data augmentation and fine tuning.

How to deploy on AWS Lambda:
Install Awscli and set it up
clone the repositiory 
for converting your tensorflow model to tensorflow lite run the script - tfliteconv.py
install flask
install zappa
install all the requirements
de

