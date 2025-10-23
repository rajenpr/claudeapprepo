# Temperature Converter Flask App

A simple Flask application that converts temperature from Celsius to Fahrenheit.

## Features

- REST API endpoint for temperature conversion
- Web interface for easy testing
- Supports both GET and POST requests
- JSON response format

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## API Usage

### Endpoint: `/convert`

#### GET Request
```bash
curl "http://localhost:5000/convert?celsius=25"
```

#### POST Request
```bash
curl -X POST http://localhost:5000/convert \
  -H "Content-Type: application/json" \
  -d '{"celsius": 25}'
```

### Response Format
```json
{
  "celsius": 25,
  "fahrenheit": 77.0,
  "formula": "F = (C × 9/5) + 32"
}
```

## Web Interface

Visit `http://localhost:5000` in your browser to access the web interface for converting temperatures.

## Conversion Formula

Fahrenheit = (Celsius × 9/5) + 32

## Examples

- 0°C = 32°F (Water freezing point)
- 100°C = 212°F (Water boiling point)
- 25°C = 77°F (Room temperature)
- -40°C = -40°F (Same in both scales)
