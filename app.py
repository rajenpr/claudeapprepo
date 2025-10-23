from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit using the formula: F = (C * 9/5) + 32"""
    return (celsius * 9/5) + 32

@app.route('/')
def home():
    """Home page with a beautiful modern UI"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Temperature Converter - Celsius to Fahrenheit</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Poppins', sans-serif;
                min-height: 100vh;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
                position: relative;
                overflow: hidden;
            }

            /* Animated background elements */
            body::before {
                content: '';
                position: absolute;
                width: 400px;
                height: 400px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 50%;
                top: -200px;
                right: -200px;
                animation: float 20s infinite ease-in-out;
            }

            body::after {
                content: '';
                position: absolute;
                width: 300px;
                height: 300px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 50%;
                bottom: -150px;
                left: -150px;
                animation: float 15s infinite ease-in-out reverse;
            }

            @keyframes float {
                0%, 100% { transform: translateY(0) translateX(0); }
                50% { transform: translateY(20px) translateX(20px); }
            }

            .container {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 30px;
                padding: 50px 40px;
                box-shadow: 0 30px 60px rgba(0, 0, 0, 0.3);
                max-width: 500px;
                width: 100%;
                position: relative;
                z-index: 1;
                backdrop-filter: blur(10px);
                animation: slideIn 0.6s ease-out;
            }

            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .header {
                text-align: center;
                margin-bottom: 40px;
            }

            .icon-wrapper {
                display: inline-block;
                font-size: 80px;
                margin-bottom: 20px;
                animation: pulse 2s infinite;
            }

            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }

            h1 {
                color: #667eea;
                font-size: 32px;
                font-weight: 700;
                margin-bottom: 10px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .subtitle {
                color: #666;
                font-size: 16px;
                font-weight: 300;
            }

            .converter-box {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 30px;
            }

            .input-group {
                position: relative;
                margin-bottom: 25px;
            }

            label {
                display: block;
                color: #333;
                font-weight: 600;
                margin-bottom: 10px;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            .input-wrapper {
                position: relative;
                display: flex;
                align-items: center;
            }

            input[type="number"] {
                width: 100%;
                padding: 18px 50px 18px 20px;
                border: 2px solid transparent;
                border-radius: 15px;
                font-size: 24px;
                font-weight: 600;
                background: white;
                color: #333;
                transition: all 0.3s ease;
                outline: none;
            }

            input[type="number"]:focus {
                border-color: #667eea;
                box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
            }

            .unit-label {
                position: absolute;
                right: 20px;
                font-size: 24px;
                color: #667eea;
                font-weight: 600;
                pointer-events: none;
            }

            .convert-btn {
                width: 100%;
                padding: 18px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 18px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 2px;
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }

            .convert-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
            }

            .convert-btn:active {
                transform: translateY(0);
            }

            .result {
                margin-top: 30px;
                padding: 25px;
                background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
                border-radius: 20px;
                opacity: 0;
                transform: scale(0.9);
                transition: all 0.4s ease;
                text-align: center;
            }

            .result.show {
                opacity: 1;
                transform: scale(1);
            }

            .result.error {
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
            }

            .result-content {
                color: white;
                font-size: 18px;
                font-weight: 600;
            }

            .result-value {
                font-size: 36px;
                font-weight: 700;
                margin: 15px 0;
                display: block;
            }

            .api-info {
                margin-top: 30px;
                padding: 20px;
                background: rgba(102, 126, 234, 0.1);
                border-radius: 15px;
                border-left: 4px solid #667eea;
            }

            .api-info h3 {
                color: #667eea;
                font-size: 16px;
                margin-bottom: 15px;
                font-weight: 600;
            }

            .api-info p {
                color: #666;
                font-size: 13px;
                line-height: 1.8;
                margin-bottom: 8px;
            }

            .api-info ul {
                margin-left: 20px;
                margin-top: 10px;
            }

            .api-info li {
                color: #666;
                font-size: 13px;
                line-height: 1.8;
                margin-bottom: 5px;
            }

            code {
                background: rgba(255, 255, 255, 0.8);
                padding: 3px 8px;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                color: #667eea;
                font-size: 12px;
            }

            .toggle-api {
                background: none;
                border: none;
                color: #667eea;
                cursor: pointer;
                font-size: 13px;
                font-weight: 600;
                margin-top: 10px;
                text-decoration: underline;
                transition: all 0.3s ease;
            }

            .toggle-api:hover {
                color: #764ba2;
            }

            .api-details {
                max-height: 0;
                overflow: hidden;
                transition: max-height 0.3s ease;
            }

            .api-details.open {
                max-height: 300px;
            }

            @media (max-width: 600px) {
                .container {
                    padding: 30px 20px;
                }

                h1 {
                    font-size: 24px;
                }

                .icon-wrapper {
                    font-size: 60px;
                }

                input[type="number"] {
                    font-size: 20px;
                    padding: 15px 45px 15px 15px;
                }

                .unit-label {
                    font-size: 20px;
                }

                .result-value {
                    font-size: 28px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="icon-wrapper">🌡️</div>
                <h1>Temperature Converter</h1>
                <p class="subtitle">Convert Celsius to Fahrenheit instantly</p>
            </div>

            <div class="converter-box">
                <div class="input-group">
                    <label for="celsius">Enter Temperature</label>
                    <div class="input-wrapper">
                        <input
                            type="number"
                            id="celsius"
                            step="0.01"
                            placeholder="0"
                            autofocus
                        >
                        <span class="unit-label">°C</span>
                    </div>
                </div>

                <button class="convert-btn" onclick="convertTemperature()">
                    Convert to Fahrenheit
                </button>
            </div>

            <div class="result" id="result"></div>

            <div class="api-info">
                <h3>🔌 API Information</h3>
                <button class="toggle-api" onclick="toggleApiDetails()">
                    Show API Usage Details
                </button>
                <div class="api-details" id="apiDetails">
                    <p><strong>Endpoint:</strong> <code>/convert</code></p>
                    <p><strong>Methods:</strong> GET, POST</p>
                    <p><strong>Examples:</strong></p>
                    <ul>
                        <li>GET: <code>/convert?celsius=25</code></li>
                        <li>POST: <code>{"celsius": 25}</code></li>
                    </ul>
                </div>
            </div>
        </div>

        <script>
            function convertTemperature() {
                const celsiusInput = document.getElementById('celsius');
                const celsius = celsiusInput.value;
                const resultDiv = document.getElementById('result');

                if (celsius === '') {
                    showResult('Please enter a temperature value', true);
                    return;
                }

                // Add loading state
                resultDiv.innerHTML = '<div class="result-content">Converting...</div>';
                resultDiv.className = 'result show';

                fetch(`/convert?celsius=${celsius}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            showResult(data.error, true);
                        } else {
                            showResult(
                                `<div class="result-content">
                                    <div>${data.celsius}°C equals</div>
                                    <span class="result-value">${data.fahrenheit}°F</span>
                                    <div style="font-size: 14px; opacity: 0.9; margin-top: 10px;">
                                        ${data.formula}
                                    </div>
                                </div>`,
                                false
                            );
                        }
                    })
                    .catch(error => {
                        showResult('Network error: ' + error.message, true);
                    });
            }

            function showResult(content, isError) {
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = typeof content === 'string' && !content.includes('<')
                    ? `<div class="result-content">${content}</div>`
                    : content;
                resultDiv.className = isError ? 'result show error' : 'result show';
            }

            function toggleApiDetails() {
                const apiDetails = document.getElementById('apiDetails');
                const toggleBtn = document.querySelector('.toggle-api');

                if (apiDetails.classList.contains('open')) {
                    apiDetails.classList.remove('open');
                    toggleBtn.textContent = 'Show API Usage Details';
                } else {
                    apiDetails.classList.add('open');
                    toggleBtn.textContent = 'Hide API Usage Details';
                }
            }

            // Allow Enter key to submit
            document.getElementById('celsius').addEventListener('keypress', function(event) {
                if (event.key === 'Enter') {
                    convertTemperature();
                }
            });

            // Auto-convert on input change (with debounce)
            let debounceTimer;
            document.getElementById('celsius').addEventListener('input', function(event) {
                clearTimeout(debounceTimer);
                if (event.target.value !== '') {
                    debounceTimer = setTimeout(() => {
                        convertTemperature();
                    }, 500);
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
