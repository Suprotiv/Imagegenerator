import openai

import os

from flask import Flask, render_template_string, request





openai.api_key = os.environ['OPENAI_API_KEY']





def generate_tutorial(components):

   response = openai.Image.create(prompt=components,

   size="1024x1024",

   response_format="url")

   image_url = response["data"][0]["url"]

   return image_url





app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def hello():

   output = ""
   if request.method == 'POST':

    components = request.form['components']
    output = generate_tutorial(components)

   return render_template_string('''

   <!DOCTYPE html >

  <html >

  <head >

   <title >Image Generator </title >

   <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">  

   <style >

   body {

   display: flex;

   justify-content: center;

   align-items: center;

   height: 100vh;

   background-color: #f5f5f5;

   }





   .container {

   background-color: #ffffff;

   border-radius: 10px;

   padding: 20px;

   box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

   }





   h1 {

   color: #333333;

   }





   .form-control {

   background-color: #f8f8f8;

   border: 1px solid #dddddd;

   color: #333333;

   }





   .btn-primary {

   background-color: #27B4E5;

   border-color: #27B4E5;

   }





   .btn-primary:hover {

   background-color: #009AD0;

   border-color: #009AD0;

   }






   .btn-secondary {

   background-color: #b0b0b0;

   border-color: #b0b0b0;

   }






   .btn-secondary:hover {

   background-color: #c2c2c2;

   border-color: #c2c2c2;

   }






   .card {

   background-color: #f8f8f8;

   border: none;

   }






   #output {

   display: block;

   margin-bottom: 20px;

   text-align: center;

   }






   #myImage {

   width: 256px;

   height: 256px;

   display: block;

   margin: 0 auto;

   }

   </style >

   <script >

   async function generateTutorial() {

   const components = document.querySelector('#components').value;

   const output = document.querySelector('#output');

   const imgElement = document.getElementById('myImage');

   const response = await fetch('/generate', {

   method: 'POST',

   body: new FormData(document.querySelector('#tutorial-form'))

   });

   const imageUrl = await response.text();
   
   document.getElementById('myImage').style.visibility = 'visible';

   imgElement.src = imageUrl;

   document.getElementById('output').style.visibility = 'hidden';

   }

   function hide() {
      document.getElementById('output').style.visibility = 'visible';
   }






   function copyToClipboard() {

   const imgElement = document.getElementById('myImage');

   const imageUrl = imgElement.src;

   const textarea = document.createElement('textarea');

   textarea.value = imageUrl;

   document.body.appendChild(textarea);

   textarea.select();

   document.execCommand('copy');

   document.body.removeChild(textarea);

   alert('Copied to clipboard');

   }

   </script >

  </head >

  <body >

   <div class="container">

   <h1 class="my-4">Custom Image Generator </h1 >

   <form id="tutorial-form" onsubmit="event.preventDefault(); generateTutorial();" class="mb-3">

   <div class="mb-3">

   <label for="components" class="form-label">Textual Description of the Image:</label >

   <input type="text" class="form-control" id="components" name="components" placeholder="Enter the Description" required >

   </div >

   <button type="submit" class="btn btn-primary" onclick="hide()">Share the Image </button >

   </form >

   <div class="card">

   <div class="card-header d-flex justify-content-between align-items-center">

   Output:

   <button class="btn btn-secondary btn-sm" onclick="copyToClipboard()">Copy </button >

   </div >

   <div class="card-body">

   <p id="output" style="visibility:hidden" >Generating an image for you...</p >

   <img id="myImage" style="visibility:hidden" src="">

   </div >

   </div >

   </div >

  </body >

  </html >






   ''',

   output=output)





@app.route('/generate', methods=['POST'])

def generate():

   components = request.form['components']

   return generate_tutorial(components)





if __name__ == '__main__':

   app.run(host='0.0.0.0', port=8080)