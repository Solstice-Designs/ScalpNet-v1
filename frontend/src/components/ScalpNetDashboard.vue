<script>
import axios from "axios";
import Plotly from "plotly.js-dist";
import Papa from "papaparse";

export default {
  name: "ScalpNetDashboard",
  data() {
    return {
      csvData: [],
      ticker: "",
      expiryDate: "",
      currentPrice: 0,
      history: {
        oneMinute: [],
        threeMinute: [],
        fiveMinute: [],
      },
      ghostBarSettings: {
        oneMinute: true,
        threeMinute: true,
        fiveMinute: true,
      },
    };
  },
  mounted() {
    this.fetchCSVData(); // Fetch the data once when component mounts
    this.scheduleDataFetch(); // Set interval to repeatedly fetch the CSV data
  },
  methods: {
    fetchCSVData() {
      // Replace with the path to your CSV file in the public directory
      const csvUrl = "/options_data.csv";

      axios
        .get(csvUrl)
        .then((response) => {
          // Use PapaParse to convert CSV string into an object
          Papa.parse(response.data, {
            header: true,
            skipEmptyLines: true,
            complete: (result) => {
              this.csvData = result.data; // Save parsed data

              if (this.csvData.length > 0) {
                this.ticker = this.csvData[0]["Ticker"];
                this.expiryDate = this.csvData[0]["Exp"];
                this.currentPrice = parseFloat(this.csvData[0]["Price"]); // Get the current price from the CSV data
              }

              this.updateHistory(); // Update historical data
              this.plotData(); // Plot the data after it's loaded
            },
          });
        })
        .catch((error) => {
          console.error("Error fetching CSV data:", error);
        });
    },
    updateHistory() {
      // Add the current data to the historical arrays
      if (this.csvData.length === 0) {
        return;
      }

      // Extracting relevant data for the history
      const callVolumes = this.csvData.map(
        (row) =>
          parseFloat(row["Call Vol"]) * parseFloat(row["Call Delta"]) * 100
      );
      const putVolumes = this.csvData.map(
        (row) =>
          -1 * parseFloat(row["Put Vol"]) * parseFloat(row["Put Delta"]) * 100
      );

      const currentDeltaVolumes = callVolumes.map(
        (call, index) => call + putVolumes[index]
      );

      // Update historical data (only retain the most recent snapshot)
      this.history.oneMinute.unshift(currentDeltaVolumes);
      if (this.history.oneMinute.length > 1) {
        this.history.oneMinute.pop(); // Limit to the most recent 1-minute snapshot
      }

      this.history.threeMinute.unshift(currentDeltaVolumes);
      if (this.history.threeMinute.length > 3) {
        this.history.threeMinute.pop(); // Limit to the most recent 3-minute snapshot
      }

      this.history.fiveMinute.unshift(currentDeltaVolumes);
      if (this.history.fiveMinute.length > 5) {
        this.history.fiveMinute.pop(); // Limit to the most recent 5-minute snapshot
      }
    },
    plotData() {
      // Check if we have data before proceeding
      if (this.csvData.length === 0) {
        console.error("No data to plot");
        return;
      }

      // Extracting relevant data from CSV
      const strikes = this.csvData.map((row) => parseFloat(row["Strike"]));
      const callVolumes = this.csvData.map(
        (row) =>
          parseFloat(row["Call Vol"]) * parseFloat(row["Call Delta"]) * 100
      );
      const putVolumes = this.csvData.map(
        (row) => parseFloat(row["Put Vol"]) * parseFloat(row["Put Delta"]) * 100
      );

      // Calculate net deltas
      const netDeltas = callVolumes.map(
        (callVolume, index) => callVolume + putVolumes[index]
      );

      // Prepare Plotly traces for Call and Put Delta-Weighted Volumes (Stacked Chart)
      const callTrace = {
        x: strikes,
        y: callVolumes,
        type: "bar",
        name: "Call Delta-Weighted Volume",
        marker: {
          color: "blue",
          opacity: 0.7,
        },
      };

      const putTrace = {
        x: strikes,
        y: putVolumes,
        type: "bar",
        name: "Put Delta-Weighted Volume",
        marker: {
          color: "red",
          opacity: 0.7,
        },
      };

      // Adding ghost bars for historical shifts (1, 3, and 5 minutes) if selected
      const ghostBars = [];
      const ghostColors = [
        "rgba(0,0,255,0.2)",
        "rgba(255,0,0,0.2)",
        "rgba(0,255,0,0.2)",
      ];
      const ghostNames = ["1-Min History", "3-Min History", "5-Min History"];
      const intervals = ["oneMinute", "threeMinute", "fiveMinute"];

      intervals.forEach((interval, index) => {
        if (
          this.ghostBarSettings[interval] &&
          this.history[interval].length > 0
        ) {
          ghostBars.push({
            x: strikes,
            y: this.history[interval][0], // Most recent snapshot for each interval
            type: "bar",
            name: ghostNames[index],
            marker: {
              color: ghostColors[index],
              opacity: 0.3,
            },
          });
        }
      });

      // Set the layout for the stacked chart for Call and Put Delta-Weighted Volumes
      const stackedLayout = {
        title: `Delta-Weighted Volume by Strike Price for ${this.ticker} (Exp: ${this.expiryDate})`,
        xaxis: {
          title: "Strike Price",
          tickvals: strikes, // Ensures every strike is shown
        },
        yaxis: {
          title: "Delta-Weighted Volume",
        },
        barmode: "relative", // Stack the bars for calls and puts
        shapes: [
          {
            type: "line",
            x0: this.currentPrice,
            x1: this.currentPrice,
            y0: Math.min(...putVolumes),
            y1: Math.max(...callVolumes),
            line: {
              color: "green",
              width: 8,
              dash: "dashdot",
            },
          },
        ],
        annotations: [
          {
            x: this.currentPrice,
            y: Math.max(...callVolumes) + 500,
            text: `Current Price: ${this.currentPrice}`,
            showarrow: true,
            arrowhead: 5,
            ax: 0,
            ay: -40,
            bgcolor: "white",
            bordercolor: "green",
            font: {
              color: "black",
              size: 12,
            },
          },
        ],
      };

      // Plot the first graph (Stacked Chart)
      Plotly.newPlot(
        "stackedChartDiv",
        [callTrace, putTrace, ...ghostBars],
        stackedLayout
      );

      // Prepare Plotly trace for Net Delta (Separate Chart)
      const netDeltaTrace = {
        x: strikes,
        y: netDeltas,
        type: "bar",
        name: "Net Delta (Calls - Puts)",
        marker: {
          color: "green",
          opacity: 0.6,
        },
      };

      // Set the layout for the Net Delta chart
      const netDeltaLayout = {
        title: `Net Delta by Strike Price for ${this.ticker} (Exp: ${this.expiryDate})`,
        xaxis: {
          title: "Strike Price",
          tickvals: strikes, // Ensures every strike is shown
        },
        yaxis: {
          title: "Net Delta",
        },
      };

      // Plot the second graph (Net Delta Chart)
      Plotly.newPlot("netDeltaChartDiv", [netDeltaTrace], netDeltaLayout);
    },
    scheduleDataFetch() {
      // Re-fetch data every 8 seconds
      setInterval(() => {
        this.fetchCSVData();
      }, 8000);
    },
  },
};
</script>

<template>
  <div>
    <h1>ScalpNet Dashboard</h1>

    <!-- Checkboxes for selecting ghost bar overlays -->
    <div class="ghost-bar-settings">
      <label
        ><input type="checkbox" v-model="ghostBarSettings.oneMinute" /> 1-Min
        Ghost Bars</label
      >
      <label
        ><input type="checkbox" v-model="ghostBarSettings.threeMinute" /> 3-Min
        Ghost Bars</label
      >
      <label
        ><input type="checkbox" v-model="ghostBarSettings.fiveMinute" /> 5-Min
        Ghost Bars</label
      >
    </div>

    <!-- Chart containers -->
    <div id="stackedChartDiv" style="width: 100%; height: 500px"></div>
    <div
      id="netDeltaChartDiv"
      style="width: 100%; height: 500px; margin-top: 50px"
    ></div>
  </div>
</template>

<style scoped>
/* Optional styles to enhance presentation */
#stackedChartDiv,
#netDeltaChartDiv {
  margin: auto;
  max-width: 900px;
}

.ghost-bar-settings {
  margin: 20px;
  display: flex;
  gap: 15px;
}
</style>
