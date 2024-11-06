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

              this.plotData(); // Plot the data after it's loaded
            },
          });
        })
        .catch((error) => {
          console.error("Error fetching CSV data:", error);
        });
    },
    plotData() {
      // Check if we have data before proceeding
      if (this.csvData.length === 0) {
        console.error("No data to plot");
        return;
      }

      // Extracting relevant data from CSV
      const strikes = this.csvData.map((row) => parseFloat(row["Strike"]));
      const callVolumes = this.csvData.map((row) =>
        parseFloat(row["Call Vol"])
      );
      const callDeltas = this.csvData.map((row) =>
        parseFloat(row["Call Delta"])
      );
      const putVolumes = this.csvData.map((row) => parseFloat(row["Put Vol"]));
      const putDeltas = this.csvData.map((row) => parseFloat(row["Put Delta"]));

      // Calculating Delta-Weighted Volume for Calls and Puts
      const callDeltaWeightedVolumes = callVolumes.map((volume, index) => {
        return volume * callDeltas[index] * 100;
      });

      const putDeltaWeightedVolumes = putVolumes.map((volume, index) => {
        return volume * putDeltas[index] * 100; // Make the Put Delta-Weighted Volume negative
      });

      // Prepare Plotly traces for Call and Put Delta-Weighted Volumes
      const callTrace = {
        x: strikes,
        y: callDeltaWeightedVolumes,
        type: "bar",
        name: "Call Delta-Weighted Volume",
        marker: {
          color: "cyan",
          opacity: 0.88,
        },
      };

      const putTrace = {
        x: strikes,
        y: putDeltaWeightedVolumes,
        type: "bar",
        name: "Put Delta-Weighted Volume",
        marker: {
          color: "purple",
          opacity: 0.7,
        },
      };

      // Set the graph layout to stack bars and display all strike values, and add the price line
      const layout = {
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
            y0: Math.min(...putDeltaWeightedVolumes), // Line extends from bottom of the y-axis
            y1: Math.max(...callDeltaWeightedVolumes), // to the top of the y-axis
            line: {
              color: "green",
              width: 6,
              dash: "dashdot",
            },
          },
        ],
        annotations: [
          {
            x: this.currentPrice,
            y: Math.max(...callDeltaWeightedVolumes) + 500, // Position slightly above the highest call bar
            text: `Current Price: $${this.currentPrice}`,
            showarrow: true,
            arrowhead: 3,
            ax: 0,
            ay: -40, // Adjusts the annotation positioning relative to the bar
            bgcolor: "white",
            bordercolor: "green",
            font: {
              color: "black",
              size: 12,
            },
          },
        ],
      };

      // Plot the graph in the chartDiv
      Plotly.newPlot("chartDiv", [callTrace, putTrace], layout);
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
    <!-- Chart container -->
    <div id="chartDiv" style="width: 100%; height: 500px"></div>
  </div>
</template>

<style scoped>
/* Optional styles to enhance presentation */
#chartDiv {
  margin: auto;
  max-width: 900px;
}
</style>
