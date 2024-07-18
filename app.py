
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
from io import BytesIO

# Define custom objects
custom_objects = {
    'SparseCategoricalCrossentropy': tf.keras.losses.SparseCategoricalCrossentropy()
}
app = Flask(__name__)
CORS(app)
model = tf.keras.models.load_model('./my_model.h5', custom_objects=custom_objects)

@app.route('/static/<string:filename>', methods=['GET'])
def sendStatic(filename):
    return send_from_directory('static', filename)

# index.html
@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')

# loginSignup.html
@app.route('/user', methods=['GET'])
def loginSignup():
    return render_template('loginSignup.html')


# imput image for processing
def preprocess_image(img):
    img = np.array(img)
    print("Image shape:", img.shape)
    
    if img.shape[-1] == 4:  
        img = img[:, :, :3]
        
    img = img / 255.0  
    return img

def predict(file):
    img = Image.open(BytesIO(file.read()))
    img = img.resize((256, 256))  
    img = preprocess_image(img)
    img = np.expand_dims(img, axis=0)  
    prediction = model.predict(img)
    print('pred ]=> ', prediction)
    return prediction

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    prediction = predict(file)
    confidence = np.max(prediction)  
    
    
    return jsonify({
        'message': 'Successfully predicted', 
        'prediction_res': str(np.argmax(prediction)),  # Send the prediction result
        'confidence': float(confidence)  # Send the confidence level
    })

if __name__ == '__main__':
    app.run(debug=True)



