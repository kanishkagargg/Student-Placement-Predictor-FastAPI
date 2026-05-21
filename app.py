from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
import pandas as pd
from model.predict import predict_output, model, MODEL_VERSION
from schema.user_input import UserInput


app = FastAPI(title="Student Placement Prediction API")

# human readable       
@app.get('/')
def home():
    return {'message':'Student Placement Prediction API'}

# machine readable
@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_loaded': model is not None
    }

@app.post('/predict')
def predict_premium(data: UserInput):

    input_df = {
        'study_efficiency': data.study_efficiency,
        'engagement_score': data.engagement_score,
        'healthy_routine': data.healthy_routine,
        'productivity_score': data.productivity_score,
        'internet_to_study_ratio': data.internet_to_study_ratio,
        'improvement_percent': data.improvement_percent,
        'attendance_category': data.attendance_category,
        'sleep_category': data.sleep_category,
        'study_level': data.study_level,
        'academic_strength': data.academic_strength,
        'discipline_score': data.discipline_score
    }


    try:

        prediction = predict_output(input_df)

        return JSONResponse(status_code=200, content={'response': prediction})
    
    except Exception as e:

        return JSONResponse(status_code=500, content=str(e))



