# HeartGuard - Heart Attack Risk Assessment

A web application that assesses the risk of heart attack using both user-provided health data and IoT sensor data.

## Features

- User-friendly web interface for health assessment
- Real-time IoT sensor integration (heart rate and SpO2)
- Risk assessment with confidence scoring
- Responsive design for all devices
- Secure data handling

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Internet connection (for IoT sensor integration)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/heart-attack-app.git
   cd heart-attack-app
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root with the following variables:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   IOT_API_URL=https://api.thingspeak.com/channels/3102827/feeds.json?results=2
   ```

## Running the Application

1. Start the development server:
   ```bash
   flask run
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Project Structure

```
heart-attack-app/
├── app.py                 # Main application file
├── requirements.txt       # Project dependencies
├── .env                  # Environment variables (not in version control)
├── .gitignore            # Git ignore file
├── README.md             # This file
├── previous_iot_data.json # Stores the latest IoT sensor data
├── static/               # Static files (CSS, JS, images)
│   ├── css/
│   └── js/
└── templates/            # HTML templates
    ├── form.html         # Assessment form
    ├── home.html         # Landing page
    ├── result.html       # Results page
    └── error.html        # Error page
```

## IoT Integration

The application can connect to an IoT device (like an Arduino or Raspberry Pi with sensors) through the ThingSpeak API. The following data is collected:

- Heart Rate (BPM)
- Blood Oxygen Level (SpO2%)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [Bootstrap](https://getbootstrap.com/) - For responsive design
- [Font Awesome](https://fontawesome.com/) - For icons
- [ThingSpeak](https://thingspeak.com/) - For IoT data collection
