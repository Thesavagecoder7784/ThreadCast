from flask import Flask, render_template, request
import requests
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = Flask(__name__)
def get_geolocation(city_name):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
    response = requests.get(geo_url)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            return data[0]['lat'], data[0]['lon']
        else:
            return None, None
    else:
        return None, None

def get_weather_data(lat, lon):
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(weather_url)
    print(response.json())
    if response.status_code == 200:
        return response.json()
    else:
        return None

explanations = {
    "thermal inner wear": "Provides excellent insulation for extremely cold temperatures.",
    "long-sleeve t-shirt": "Comfortable and warm for indoor or mild cool conditions.",
    "long-sleeve t-shirt or blouse": "Suitable for cooler weather, providing warmth without overheating.",
    "short-sleeve t-shirt or blouse": "Ideal for mild temperatures and indoor environments.",
    "light tank top or breathable t-shirt": "Perfect for hot weather to keep you cool and comfortable.",
    "insulated pants or leggings": "Keeps your legs warm in freezing conditions, especially outdoors.",
    "warm trousers": "Comfortable and warm, suitable for indoor settings.",
    "jeans or warm trousers": "A versatile choice for cooler weather and casual activities.",
    "comfortable pants or casual trousers": "Perfect for mild weather and all-day comfort.",
    "shorts or light skirt": "Allows ventilation and keeps you cool in hot conditions.",
    "windbreaker or warm jacket": "Protects against wind chill and provides warmth.",
    "raincoat or waterproof jacket": "Essential for keeping dry during rainy weather.",
    "umbrella": "Provides protection from rain without overheating.",
    "snow boots": "Insulated and waterproof footwear for snowy conditions.",
    "waterproof outerwear": "Shields against snow and wet conditions, keeping you dry and warm.",
    "sunglasses": "Protects your eyes from UV rays during clear, sunny weather.",
    "blazer or formal jacket": "Adds a polished and professional appearance for formal settings.",
    "dress shoes": "Complements formal attire while ensuring comfort and style.",
    "formal light trousers or skirt": "Suitable for formal occasions in warmer weather.",
    "activewear": "Designed for flexibility and comfort during physical activities.",
    "trainers or running shoes": "Provides support and comfort for sporty or active occasions.",
    "light athletic jacket": "Adds a layer of warmth during outdoor activities in cooler weather.",
    "comfortable walking shoes": "Reduces fatigue and supports your feet during long walks.",
    "professional attire": "Projects a professional image, ideal for business meetings.",
    "stylish outfit": "Suitable for social gatherings, making you look fashionable and confident.",
    "cardigan or pullover": "A light layer perfect for staying warm in indoor settings.",
    "layers for easy removal": "Allows flexibility in transit when moving between environments."
}

def enhanced_outfit_recommendations(weather_data, user_preferences):
    outfit = {
        "base_layer": None,
        "mid_layer": None,
        "outer_layer": None,
        "bottoms": None,
        "footwear": None,
        "accessory": None
    }

    explanations = {}

    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    description = weather_data['weather'][0]['description']
    wind_speed = weather_data['wind']['speed']
    humidity = weather_data['main']['humidity']

    # Extract user preferences
    style = user_preferences.get('style', 'casual')
    environment = user_preferences.get('environment', 'outside')
    event = user_preferences.get('event', 'general')

    # Base Layer
    if temp < 0:
        outfit["base_layer"] = "thermal inner wear" if environment != "inside" else "long-sleeve t-shirt"
        explanations[outfit["base_layer"]] = "Provides warmth appropriate for freezing or indoor temperatures."
    elif temp < 10:
        outfit["base_layer"] = "long-sleeve t-shirt"
        explanations[outfit["base_layer"]] = "Ideal for cooler weather."
    elif temp < 21:
        outfit["base_layer"] = "short-sleeve t-shirt"
        explanations[outfit["base_layer"]] = "Suitable for mild weather."
    else:
        if style == "casual":
            outfit["base_layer"] = "breathable t-shirt"
            explanations[outfit["base_layer"]] = "Keeps you cool in warm weather."
        elif style == "formal":
            outfit["base_layer"] = "semi-formal shirt"
            explanations[outfit["base_layer"]] = "Keeps you cool in warm weather."

    # Mid Layer
    if temp < 0:
        outfit["mid_layer"] = "fleece jacket or heavy sweater"
        explanations[outfit["mid_layer"]] = "Provides an additional layer of insulation in freezing temperatures."
    elif temp < 10:
        outfit["mid_layer"] = "light sweater or hoodie"
        explanations[outfit["mid_layer"]] = "Adds moderate warmth for cooler weather."
    elif temp < 21:
        outfit["mid_layer"] = "light cardigan or hoodie"
        explanations[outfit["mid_layer"]] = "Useful for layering in mild temperatures."

    # Outer Layer
    if temp < 0 and "snow" in description or wind_speed > 15:
        outfit["outer_layer"] = "heavy winter coat"
        explanations[outfit["outer_layer"]] = "Essential for retaining heat in freezing or windy conditions."
    elif temp < 10 or wind_speed > 15:
        outfit["outer_layer"] = "windproof jacket"
        explanations[outfit["outer_layer"]] = "Protects against cool winds."
    elif "rain" in description or "drizzle" in description:
        outfit["outer_layer"] = "waterproof rain jacket"
        explanations[outfit["outer_layer"]] = "Keeps you dry in wet conditions."

    # Bottoms
    if temp < 0:
        outfit["bottoms"] = "insulated pants or thermal leggings" if environment != "inside" else "warm trousers"
        explanations[outfit["bottoms"]] = "Appropriate for extreme cold or indoor settings."
    elif temp < 10:
        outfit["bottoms"] = "jeans or warm trousers"
        explanations[outfit["bottoms"]] = "Versatile option for cooler weather."
    elif temp < 21:
        outfit["bottoms"] = "comfortable pants or joggers"
        explanations[outfit["bottoms"]] = "Suitable for mild weather."
    else:
        outfit["bottoms"] = "shorts or light skirt"
        explanations[outfit["bottoms"]] = "Keeps you cool in hot weather."

    # Footwear
    if "rain" in description or "drizzle" in description:
        outfit["footwear"] = "rain boots or waterproof sneakers"
        explanations[outfit["footwear"]] = "Protects your feet from getting wet."
        outfit["accessory"] = "umbrella"
        explanations[outfit["accessory"]] = "Provides protection from rain without overheating."
    elif "snow" in description:
        outfit["footwear"] = "warm boots"
        explanations[outfit["footwear"]] = "Provides insulation and traction in snow."
    elif temp < 0:
        outfit["footwear"] = "insulated boots"
        explanations[outfit["footwear"]] = "Keeps your feet warm in freezing temperatures."
    else:
        outfit["footwear"] = "comfortable sneakers"
        explanations[outfit["footwear"]] = "Ideal for mild weather."

    # Accessories
    if humidity < 30 and temp < 10:
        outfit["accessory"] = "hydrating skincare or lip balm"
        explanations["hydrating skincare or lip balm"] = "Protects skin from dryness in low humidity."

    print(outfit.values())
    return outfit, explanations


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    city = request.form.get('city')
    style = request.form.get('style')
    environment = request.form.get('environment')
    event = request.form.get('event')

    user_preferences = {
        "style": style,
        "environment": environment,
        "event": event
    }

    lat, lon = get_geolocation(city)
    if lat is not None and lon is not None:
        weather_data = get_weather_data(lat, lon)
        if weather_data:
            outfit, explanations = enhanced_outfit_recommendations(weather_data, user_preferences)
            # Filter out None values from the outfit dictionary
            filtered_outfit = {key: value for key, value in outfit.items() if value is not None}
            return render_template('results.html', 
                                   city=city, 
                                   weather_data=weather_data, 
                                   recommendations=filtered_outfit.values(), 
                                   explanations=explanations)
        else:
            return render_template('error.html', message="Failed to fetch weather data.")
    else:
        return render_template('error.html', message="City not found!")

if __name__ == '__main__':
    app.run(debug=True)
