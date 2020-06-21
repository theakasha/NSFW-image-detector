![](nsfw.jpeg)
# NSFW-Image-Detector
Demo https://hy1al8aeg7.execute-api.ap-south-1.amazonaws.com/dev   
 What it does?  
It detects Not Safe For Work Images by calculating a NSFW score and classifying them into five categories:     Drawing,Hentai,Neutral,Porn,Sexy.Images can be uploaded directly from the client's computer or through a GET request with the source of the image.    
eg: https://hy1al8aeg7.execute-api.ap-south-1.amazonaws.com/dev/upload?text=img_src

What is it?  
It's a Convolutional Neural Network model deployed using Flask ,tensorflow-lite ,AWS lambda + API gateway using zappa.

* The inception v3 model is trained and finetuned on the dataset. https://github.com/alex000kim/nsfw_data_scraper .I used transfer learning for training the model.    

* To make sure the deployment package size is within the memory limits of aws lambda,I converted my model from tensorflow to tensorflow lite. For installing just the tf-lite interpreter check the official documentation https://www.tensorflow.org/lite/guide/python  
* For installing tf-lite dependencies on lambda, you need to make sure that zappa detects tf-lite. Just copy tf-lite folder from virtualenv/lib/python/site-packages to the top-level folder in lambda : https://www.reddit.com/r/aws/comments/93jhgi/how_can_i_add_third_party_python_dependencies_to/
The model is present in an s3 bucket and gets downloaded in the predictions.py script using Boto3 to the lambda s3 bucket.
I built a flask api for serving my model's predictions. Refer to the official flask documentation. 


The motive:  
The main purpose behind this is to use Atificial intelligence to provide users with a safe browsing experience  

This is a part of a larger project.I am currently working on a chrome extension which would detect the NSFW images on the browser & blur them out or even better replace them with images of kittens:)
 
  
  
  
