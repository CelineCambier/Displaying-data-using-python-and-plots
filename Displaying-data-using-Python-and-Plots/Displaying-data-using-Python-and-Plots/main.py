import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
from flask import Flask, send_file
import io
import base64

app = Flask(__name__)

# Climate data
years = [2000, 2005, 2010, 2015, 2020]
temp_anomalies = [0.8, 0.9, 1.0, 1.2, 1.3]  # °C deviation from a baseline
co2_emissions = [25, 30, 35, 40, 45]  # in billions of metric tons

@app.route('/')
def show_climate_charts():
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Temperature anomalies chart
    ax1.plot(years, temp_anomalies, 'ro-', linewidth=2, markersize=8)
    ax1.set_title('Global Temperature Anomalies', fontsize=16, fontweight='bold')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Temperature Anomaly (°C)')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1.5)
    
    # CO2 emissions chart  
    ax2.bar(years, co2_emissions, color='skyblue', alpha=0.7, edgecolor='navy')
    ax2.set_title('Global CO2 Emissions', fontsize=16, fontweight='bold')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('CO2 Emissions (Billion Metric Tons)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot to bytes
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    img_buffer.seek(0)
    plt.close()
    
    # Convert to base64 for HTML display
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Climate Data Visualization</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 1000px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #2c3e50;
                text-align: center;
                margin-bottom: 30px;
            }}
            .chart {{
                text-align: center;
                margin: 20px 0;
            }}
            .description {{
                background-color: #ecf0f1;
                padding: 20px;
                border-radius: 5px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌍 Climate Data Dashboard</h1>
            <div class="chart">
                <img src="data:image/png;base64,{img_base64}" alt="Climate Charts" style="max-width: 100%; height: auto;">
            </div>
            <div class="description">
                <h3>About This Data</h3>
                <p><strong>Temperature Anomalies:</strong> Shows the deviation from historical baseline temperatures from 2000-2020.</p>
                <p><strong>CO2 Emissions:</strong> Global carbon dioxide emissions in billions of metric tons over the same period.</p>
                <p>This visualization demonstrates the correlation between rising temperatures and increasing CO2 emissions.</p>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)