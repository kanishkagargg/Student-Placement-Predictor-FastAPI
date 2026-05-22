# Student Placement Prediction via FastAPI

This project demonstrates a local student placement prediction system built with FastAPI as the middleware between a trained machine learning model and a Streamlit frontend.

## What this project is about

The application predicts a student's placement or performance category using student academic and behavior data. It validates user input, computes derived features, calls a backend prediction model, and returns a structured prediction response.

## Tech stack

- Python
- FastAPI for the API layer
- Streamlit for the frontend user interface
- Pydantic for input validation and feature engineering
- Pickle for serialized model loading
- scikit-learn / RandomForestClassifier-compatible model inference
- Requests for frontend API calls

## Architecture & separation of concerns

The project follows a clean separation of responsibilities:

- `app.py` - FastAPI application and endpoint definitions (`/`, `/health`, `/predict`)
- `schema/user_input.py` - Pydantic request model with validation and computed feature generation
- `model/predict.py` - Model loading and prediction logic, isolated from web handling
- `frontend.py` - Streamlit UI that sends input to the FastAPI endpoint and displays results

This architecture keeps the API layer, data validation/feature engineering, and model inference separate so the application is easier to maintain and extend.

## FastAPI as the middleware

FastAPI is used as the mid layer between the frontend and the ML model backend. The Streamlit frontend sends JSON data to FastAPI, which then:

1. validates and parses request data using `schema/user_input.py`
2. computes engineered features such as `study_efficiency`, `engagement_score`, and `discipline_score`
3. forwards the feature vector to `model/predict.py`
4. returns the prediction result to the frontend

This design allows the ML model to remain decoupled from the UI, which is especially important for production when the model backend can be deployed independently on cloud services like AWS.

## API endpoints

- `GET /` - Basic welcome route
- `GET /health` - Health check with model version and load status
- `POST /predict` - Prediction endpoint

### Example request

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "previous_score": 75,
    "study_hours": 6,
    "attendance": 85,
    "sleep_hours": 7,
    "assignments_completed": 8,
    "internet_usage": 2,
    "exam_score": 80
  }'
```

### Example response

```json
{
  "response": {
    "predicted_category": "Placed",
    "confidence": 0.92,
    "class_probabilities": {
      "Placed": 0.92,
      "Not Placed": 0.08
    }
  }
}
```

> Note: Because this is a local setup, the API URL is `http://127.0.0.1:8000/predict`. For production, deploy the FastAPI service to a cloud provider such as AWS, and update the frontend to use the deployed endpoint.

## How to run

### 1. Create and activate the environment

```bash
python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start the FastAPI backend

```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

### 3. Start the Streamlit frontend

```bash
streamlit run frontend.py
```

### 4. Open the apps

- FastAPI docs: `http://127.0.0.1:8000/docs`
- Streamlit UI: follow the URL printed by Streamlit in the terminal

## Notes

- The model is loaded from `model/student_performance_model.pkl` in `model/predict.py`.
- `schema/user_input.py` performs derived feature computation so that the prediction layer receives a fully prepared input vector.
- `frontend.py` currently uses `http://127.0.0.1:8000/predict` for local development.

## Demo

A demo video is included in this repository:

- `Student Placement Prediction via FastAPI.mp4`

Use this file to review a walkthrough of the app and how the FastAPI backend and Streamlit frontend interact.

## Improvements and production considerations

- Deploy FastAPI on cloud platforms like AWS EC2, AWS Lambda, or AWS Elastic Beanstalk
- Use HTTPS for secure API communication
- Add authentication and rate limiting if exposing the API publicly
- Replace the local pickle model with a model registry or managed service for production-scale deployment
- Add logging, monitoring, and error tracking for reliability

## Summary

This project demonstrates a clean, local end-to-end ML deployment pattern:

- Streamlit frontend for user input
- FastAPI middleware for API handling and validation
- Model backend for prediction
- Separation of concerns for maintainability and easier production migration
