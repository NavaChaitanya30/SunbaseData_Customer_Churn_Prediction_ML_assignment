from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict_churn():
    try:
        # Get data from the request JSON
        data = request.json
        # print("data in req",data)
        # Preprocess the input data
        preprocessed_data = preprocess_data(data)
        # print('data after pre-processed\n',preprocessed_data)
        # print(preprocessed_data.columns)
        # Perform prediction using the trained model
        #prediction = predict_using_model(preprocessed_data)
        # Load the trained model
       
        model = joblib.load('/home/lenovo/Documents/internshala/Trained_models/SVC_5_cols.pkl')
        # print(model.feature_names_in_)
        
        # Predict churn using the model
        prediction = model.predict(preprocessed_data)
        print("prediction",prediction)
        prediction = True if prediction[0] == 1 else False
        print("prediction",prediction)
        # Return the prediction as a JSON response
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)})

def preprocess_data(input_data):
    """
    Preprocess the input data before making a prediction.
    
    Parameters:
    input_data (dict): Dictionary containing input data fields.
    
    Returns:
    preprocessed_data (pd.DataFrame): Preprocessed data ready for prediction.
    """
    # Convert the input data into a DataFrame
    input_df = pd.DataFrame([input_data])

    # Perform data preprocessing steps
    preprocessed_data = input_df.copy()
    preprocessed_data.drop(columns=['CustomerID','Name','Location'],axis=1,inplace=True)
    preprocessed_data['Gender'] = (preprocessed_data['Gender'] == 'Male').astype(int)

    return preprocessed_data

# def predict_using_model(data):
#     # Load the trained model
#     model = joblib.load('../Trined_models/SVC_5_cols.pkl')
#     print(model)
#     # Predict churn using the model
#     prediction = model.predict(data)
    
#     return prediction[0]

if __name__ == '__main__':
    app.run(debug=True)
