# ScalpNet Dashboard Prototype

ScalpNet is a trading analysis platform designed to visualize and help traders pinpoint market opportunities in the options market using delta-weighted volume metrics and liquidity analysis. This prototype version uses a makeshift API in the form of an Excel sheet that outputs options data to a CSV file every 8 seconds. The front-end is built with Vue.js, Plotly, and other JavaScript libraries, while the back-end processes the CSV data, creating insights displayed in dynamic charts.

![image](https://github.com/user-attachments/assets/e0508cd6-4d1c-40de-b50c-2bc672d6040c)

## Key Features

1. **Data Visualization for Delta-Weighted Volume**
   - Display delta-weighted volume for call and put options across different strike prices.
   - The chart provides visual clues about where significant liquidity cliffs exist, helping traders identify entry and exit points.

2. **Net Delta Analysis**
   - Visualize net delta (Calls - Puts) by strike price to understand where the market is positioned (e.g., areas where buyers or sellers dominate).

3. **Dynamic Overlay for Historical Data**
   - Ghost bars for 1, 3, and 5-minute intervals to visualize shifts in market conditions over time.
   - The overlays help users track changes in sentiment and flow within a short timeframe.

4. **Real-Time Update**
   - The system updates the data every 8 seconds, pulling from a CSV file that is continually written by the makeshift API.

5. **Current Price Marker**
   - A moving slider and a floating text bubble display the current price to help traders understand the market relative to the strikes.

6. **Settings for Customizing the Chart**
   - Users can choose which historical overlays they wish to see using checkboxes. This adds flexibility to the visualization and allows traders to focus on the timeframe they are most interested in.

## Installation Instructions

### Prerequisites
- **Node.js** (Version 14 or above)
- **npm** (Usually installed with Node.js)
- **Python** (For back-end CSV data handling)
- **Vue.js CLI**

### Getting Started

1. **Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd ScalpNetPrototype
   ```

2. **Install Dependencies**
   Navigate to the `frontend` directory and install the required packages:
   ```bash
   cd frontend
   npm install
   ```

   Navigate to the `backend` directory and install Python dependencies:
   ```bash
   cd ../backend
   pip install -r requirements.txt
   ```

3. **Run the Back-End Data Handler**
   Ensure that the Excel sheet is being updated by the makeshift API every 4 seconds, then run the Python back-end script to create time series data:
   ```bash
   python data_scheduler.py
   ```

4. **Run the Front-End Application**
   Go back to the `frontend` directory and run the Vue.js development server:
   ```bash
   cd ../frontend
   npm run serve
   ```

   The application should be available at `http://localhost:8080`.

## Directory Structure

```
ScalpNetPrototype/
|
|-- backend/
|   |-- config/
|   |   |-- config.json
|   |-- data_handler.py
|   |-- data_scheduler.py
|
|-- frontend/
|   |-- public/
|   |   |-- options_data.csv
|   |-- src/
|       |-- components/
|       |   |-- ScalpNetDashboard.vue
|       |-- router/
|       |   |-- index.js
|       |-- views/
|       |   |-- HomeView.vue
|       |-- main.js
|-- README.md
```

## Detailed Breakdown

### Back-End Components

- **data_handler.py**: Reads the Excel file that contains the options data and extracts the headers and rows, exporting them to a CSV file (`options_data.csv`).

- **data_scheduler.py**: Executes `data_handler.py` every 8 seconds, ensuring the CSV file always contains up-to-date information.

- **config/config.json**: Contains configuration details (such as paths) to manage the back-end processing.

### Front-End Components

- **ScalpNetDashboard.vue**: The main component that displays the trading charts, including the delta-weighted volume for calls and puts, as well as the net delta visualization.

- **router/index.js**: Sets up routes for the app, providing navigation between the home view and the ScalpNet Dashboard.

- **main.js**: Bootstraps the Vue application, setting up the router and rendering the main component.

### Visualization Tools

- **Plotly.js**: Used to render charts for delta-weighted volume and net delta, allowing users to visualize the liquidity and market positioning effectively.

- **PapaParse**: A JavaScript library to parse CSV data in the browser for quick visualization.

## How It Works

- **Excel Makeshift API**: The Excel file is updated every 4 seconds and saved to disk, creating a real-time snapshot of the market. The Python script (`data_handler.py`) reads this data, processes it, and outputs it as a CSV file.

- **Data Handling**: The CSV file is read by the front-end using Axios and PapaParse, with the data fed into the Plotly charts to create actionable insights for users.

- **Delta-Weighted Volume**: The delta-weighted volume metric is a way to account for the impact of options contracts with respect to the underlying asset price. Call and Put delta volumes are stacked together to provide an overall sense of liquidity distribution.

## Future Enhancements

- **User Authentication**: Implement a robust login and registration system for multiple users.
- **Real API Integration**: Use a proper options data API (like Schwab or similar) to replace the makeshift Excel API.
- **Expanded Visualizations**: Introduce additional metrics like Vanna and Gamma Exposure (GEX) to provide more insights.
- **Real-Time Alerts**: Add alert functionality to notify users when a liquidity event or price threshold is met.

## Known Issues

- The makeshift Excel API relies on consistent saving and may lead to gaps if not maintained correctly.
- Visualization may lag slightly due to the interval-based data fetching mechanism. A websocket-based update could improve this in the future.

## Contributing
If you're interested in contributing to ScalpNet, feel free to fork the repository and submit a pull request. Let's collaborate to make trading analytics smarter and more intuitive.

## License
ScalpNet is released under the MIT License. See `LICENSE` for details.

---
Thank you for trying out ScalpNet! Your feedback and contributions are greatly appreciated.



