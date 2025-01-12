from flask import Flask, render_template, request
import pandas as pd
import tensorflow as tf
import numpy as np
import csv
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import requests

app = Flask(__name__)

API_KEY = "8be64bf64b90d77b92aa5cc332f90180"  # Replace with your API key

# ========== Helper Functions ==========
def get_geolocation(city_name):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
    response = requests.get(geo_url)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            return data[0]['lat'], data[0]['lon']
    return None, None

def get_weather_data(lat, lon):
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(weather_url)
    if response.status_code == 200:
        return response.json()
    return None

def log_user_data(city, weather_data, user_preferences, outfit):
    log_entry = {
        "timestamp": datetime.now(),
        "city": city,
        "temp": weather_data['main']['temp'],
        "feels_like": weather_data['main']['feels_like'],
        "wind_speed": weather_data['wind']['speed'],
        "humidity": weather_data['main']['humidity'],
        "description": weather_data['weather'][0]['description'],
        "style": user_preferences.get("style", "casual"),
        "environment": user_preferences.get("environment", "outside"),
        "event": user_preferences.get("event", "general"),
        "outfit": outfit
    }
    with open("user_data.csv", mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=log_entry.keys())
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(log_entry)

def train_neural_model():
    data = pd.read_csv("user_data.csv")
    features = pd.get_dummies(data[["temp", "feels_like", "wind_speed", "humidity", "style", "environment", "event"]])
    labels = data["outfit"]

    encoder = OneHotEncoder()
    labels_encoded = encoder.fit_transform(labels.values.reshape(-1, 1)).toarray()

    X_train, X_test, y_train, y_test = train_test_split(features, labels_encoded, test_size=0.2, random_state=42)

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation="relu", input_dim=X_train.shape[1]),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(labels_encoded.shape[1], activation="softmax")
    ])
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))
    model.save("outfit_neural_model.h5")
    return encoder

def predict_with_neural_model(weather_data, user_preferences, encoder):
    input_data = pd.DataFrame([{
        "temp": weather_data["main"]["temp"],
        "feels_like": weather_data["main"]["feels_like"],
        "wind_speed": weather_data["wind"]["speed"],
        "humidity": weather_data["main"]["humidity"],
        "style": user_preferences.get("style", "casual"),
        "environment": user_preferences.get("environment", "outside"),
        "event": user_preferences.get("event", "general")
    }])
    input_data = pd.get_dummies(input_data)

    training_cols = pd.read_csv("user_data.csv").columns
    for col in training_cols:
        if col not in input_data.columns:
            input_data[col] = 0

    model = tf.keras.models.load_model("outfit_neural_model.h5")
    predictions = model.predict(input_data)
    outfit = encoder.inverse_transform(predictions)
    return outfit[0]

def rule_based_outfit_recommendations(weather_data, user_preferences):
    temp = weather_data['main']['temp']
    description = weather_data['weather'][0]['description']
    style = user_preferences.get('style', 'casual')

    outfit = {"base_layer": None, "mid_layer": None, "outer_layer": None, "bottoms": None, "footwear": None}
    explanations = {}

    # Example symbolic logic
    if temp < 0:
        outfit["base_layer"] = "thermal inner wear"
        explanations["thermal inner wear"] = "Keeps you warm in extreme cold."
    elif temp < 10:
        outfit["base_layer"] = "long-sleeve t-shirt"
        explanations["long-sleeve t-shirt"] = "Ideal for cool weather."
    else:
        outfit["base_layer"] = "short-sleeve t-shirt"
        explanations["short-sleeve t-shirt"] = "Comfortable for warmer weather."

    return outfit, explanations

def enhanced_outfit_recommendations(weather_data, user_preferences, encoder):
    symbolic_outfit, symbolic_explanations = rule_based_outfit_recommendations(weather_data, user_preferences)
    neural_outfit = predict_with_neural_model(weather_data, user_preferences, encoder)

    final_outfit = symbolic_outfit.copy()
    final_explanations = symbolic_explanations.copy()

    if neural_outfit not in final_outfit.values():
        final_outfit["neural_suggestion"] = neural_outfit
        final_explanations[neural_outfit] = "Based on historical preferences."

    return final_outfit, final_explanations

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    city = request.form.get('city')
    style = request.form.get('style')
    environment = request.form.get('environment')
    event = request.form.get('event')

    user_preferences = {"style": style, "environment": environment, "event": event}

    lat, lon = get_geolocation(city)
    if lat is not None and lon is not None:
        weather_data = get_weather_data(lat, lon)
        if weather_data:
            encoder = train_neural_model()  # Train model on startup or use a pre-trained model
            outfit, explanations = enhanced_outfit_recommendations(weather_data, user_preferences, encoder)
            log_user_data(city, weather_data, user_preferences, outfit)
            return render_template('results.html', city=city, recommendations=outfit.values(), explanations=explanations)
        else:
            return render_template('error.html', message="Failed to fetch weather data.")
    else:
        return render_template('error.html', message="City not found!")

if __name__ == '__main__':
    app.run(debug=True)
