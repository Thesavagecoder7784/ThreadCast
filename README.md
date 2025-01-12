# ThreadCast
Smart outfit recommendations tailored to weather and style preferences, powered by Flask and Machine Learning

## Project Description: Smart Weather-Based Outfit Recommendations
This project is a Python-based Flask application that provides smart, weather-driven outfit recommendations tailored to user preferences. It combines real-time weather data with user-defined inputs (style, environment, and event type) to generate personalized clothing suggestions, ensuring comfort and practicality in various conditions.

## Key Features:
- Real-Time Weather Integration:
  Utilizes the OpenWeatherMap API to fetch geolocation and real-time weather data for any city.
  Retrieves essential weather parameters, including temperature, humidity, wind speed, and weather conditions.
- Dynamic Outfit Recommendations:
  Recommends clothing layers (base, mid, outer), bottoms, footwear, and accessories based on weather conditions.
  Adapts recommendations for extreme temperatures, rain, snow, wind, and humidity.
- User Preferences:
  Considers style preferences (casual, formal, sporty).
  Adapts suggestions for different environments (inside, outside) and events (general, meeting, workout).
- Comprehensive Explanations: Each recommendation includes an explanation of its suitability for the weather and scenario, enhancing user understanding.
- Interactive Web Interface: A clean and simple web form allows users to input their city and preferences.

Outputs tailored outfit recommendations alongside weather details.

## How It Works:
### Input:
The user provides a city name, preferred style, environment, and event type.
### Weather Data Retrieval:
The app fetches latitude and longitude for the city, and then retrieves detailed weather data.
### Outfit Recommendation:
The app processes weather data and user preferences to recommend a complete outfit, including explanations for each suggestion.
### Output:
Recommendations are displayed on the results page, ensuring the user is prepared for any weather condition.

## Example Use Case:
Input: A user in Hammond, Indiana, on January 12, 2025, wants outfit recommendations. They submit the following preferences:

Style: Casual
Environment: Outside
Event: General
Weather Data Retrieved:

Location: Hammond, IN, USA
Temperature: -0.36°C
Feels Like: -6.24°C
Condition: Overcast clouds
Wind Speed: 6.69 m/s
Humidity: 87%
Visibility: 402 meters
Outfit Recommendations:

Base Layer: Thermal inner wear
Provides excellent insulation for extremely cold temperatures.
Mid Layer: Fleece jacket or heavy sweater
Adds layer of insulation for freezing temperatures.
Outer Layer: Windproof jacket
Protects against wind chill and retains warmth.
Bottoms: Insulated pants or thermal leggings
Keeps your legs warm in freezing outdoor conditions.
Footwear: Insulated boots
Ensures warmth and protection in extreme cold.
Accessory: None recommended for this scenario.

## Technologies Used:
- Flask: This is used to build the web application.
- OpenWeatherMap API: To fetch real-time weather data.
- Python: For back-end logic and data processing.
- HTML & CSS: This is used to render the user interface.

## Why This Project Stands Out:
- Bridges the gap between weather forecasting and everyday decisions.
- Demonstrates integration of APIs and user-centric functionality.
- Highly adaptable to e-commerce, travel, or fashion industries.

## Future Enhancements:
- Machine Learning: Use user feedback and historical weather data to improve recommendations.
- E-Commerce Integration: Link recommended items to online stores.
- Mobile App: Expand the project to a mobile-first design for broader usability.

![Example](https://github.com/Thesavagecoder7784/images/blob/master/ThreadCast%20Homepage.png?raw=true)

![Results](https://github.com/Thesavagecoder7784/images/blob/master/ThreadCastResults.png?raw=true)
