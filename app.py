from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit using the formula: F = (C * 9/5) + 32"""
    return (celsius * 9/5) + 32

@app.route('/')
def home():
    """Home page with a simple form to test the API"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Temperature Converter</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
            }
            .container {
                border: 2px solid #4CAF50;
                border-radius: 10px;
                padding: 30px;
                background-color: #f9f9f9;
            }
            h1 {
                color: #4CAF50;
                text-align: center;
            }
            .form-group {
                margin: 20px 0;
            }
            label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }
            input[type="number"] {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                box-sizing: border-box;
            }
            button {
                width: 100%;
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background-color: #45a049;
            }
            .result {
                margin-top: 20px;
                padding: 15px;
                background-color: #e8f5e9;
                border-radius: 5px;
                display: none;
            }
            .result.show {
                display: block;
            }
            .api-info {
                margin-top: 30px;
                padding: 15px;
                background-color: #fff3cd;
                border-radius: 5px;
            }
            code {
                background-color: #f4f4f4;
                padding: 2px 5px;
                border-radius: 3px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Temperature Converter</h1>
            <p style="text-align: center;">Convert Celsius to Fahrenheit</p>

            <div class="form-group">
                <label for="celsius">Temperature in Celsius:</label>
                <input type="number" id="celsius" step="0.01" placeholder="Enter temperature in Celsius">
            </div>

            <button onclick="convertTemperature()">Convert</button>

            <div class="result" id="result"></div>

            <div class="api-info">
                <h3>API Usage:</h3>
                <p><strong>Endpoint:</strong> <code>/convert</code></p>
                <p><strong>Method:</strong> GET or POST</p>
                <p><strong>Parameters:</strong></p>
                <ul>
                    <li>GET: <code>/convert?celsius=25</code></li>
                    <li>POST: Send JSON <code>{"celsius": 25}</code></li>
                </ul>
            </div>
        </div>

        <script>
            function convertTemperature() {
                const celsius = document.getElementById('celsius').value;
                const resultDiv = document.getElementById('result');

                if (celsius === '') {
                    alert('Please enter a temperature value');
                    return;
                }

                fetch(`/convert?celsius=${celsius}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            resultDiv.innerHTML = `<strong>Error:</strong> ${data.error}`;
                            resultDiv.className = 'result show';
                            resultDiv.style.backgroundColor = '#ffebee';
                        } else {
                            resultDiv.innerHTML = `
                                <strong>Result:</strong><br>
                                ${data.celsius}°C = ${data.fahrenheit}°F
                            `;
                            resultDiv.className = 'result show';
                            resultDiv.style.backgroundColor = '#e8f5e9';
                        }
                    })
                    .catch(error => {
                        resultDiv.innerHTML = `<strong>Error:</strong> ${error.message}`;
                        resultDiv.className = 'result show';
                        resultDiv.style.backgroundColor = '#ffebee';
                    });
            }

            // Allow Enter key to submit
            document.getElementById('celsius').addEventListener('keypress', function(event) {
                if (event.key === 'Enter') {
                    convertTemperature();
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/convert', methods=['GET', 'POST'])
def convert_temperature():
    """
    Convert temperature from Celsius to Fahrenheit

    Accepts:
    - GET request with query parameter: /convert?celsius=25
    - POST request with JSON body: {"celsius": 25}

    Returns:
    - JSON response with both celsius and fahrenheit values
    """
    try:
        if request.method == 'POST':
            # Handle POST request with JSON body
            data = request.get_json()
            if not data or 'celsius' not in data:
                return jsonify({
                    'error': 'Missing celsius parameter in JSON body'
                }), 400
            celsius = float(data['celsius'])
        else:
            # Handle GET request with query parameter
            celsius_param = request.args.get('celsius')
            if celsius_param is None:
                return jsonify({
                    'error': 'Missing celsius parameter in query string'
                }), 400
            celsius = float(celsius_param)

        # Convert to Fahrenheit
        fahrenheit = celsius_to_fahrenheit(celsius)

        return jsonify({
            'celsius': celsius,
            'fahrenheit': round(fahrenheit, 2),
            'formula': 'F = (C × 9/5) + 32'
        })

    except ValueError:
        return jsonify({
            'error': 'Invalid temperature value. Please provide a valid number.'
        }), 400
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
