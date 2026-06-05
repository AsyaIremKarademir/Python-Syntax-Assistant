AI-Based Python Syntax Error Detection Assistant
Most code editors just highlight standard errors — they don't analyze code at a structural level using machine learning. This project aims to:
Automatically detect syntax risks using Abstract Syntax Tree (AST) analysis
Evaluate code blocks using NLP-driven TF-IDF feature extraction
Predict whether code is "High Risk (Faulty)" or "Low Risk (Clean)" via a Random Forest classifier
Display a dynamic Confidence Score to show how certain the model is about its prediction
Provide a clean, user-friendly Streamlit dashboard for instant code checks

Tech I Used:
Python (main language)
Scikit-learn (for machine learning model)
Streamlit (for building the web UI)
Pandas & NumPy (for data handling)
