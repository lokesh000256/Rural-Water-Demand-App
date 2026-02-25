
from flask import Flask, render_template, request, send_file
import matplotlib 
matplotlib.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/forecast", methods=["POST"])
def forecast():
    base_year = int(request.form["base_year"])
    base_population = int(request.form["population"])
    growth_rate = float(request.form["growth_rate"]) / 100
    lpcd = float(request.form["lpcd"])
    years = int(request.form["years"])

    data = []

    for y in range(years + 1):
        year = base_year + y
        population = base_population * ((1 + growth_rate) ** y)

        domestic = population * lpcd
        institutional = 0.10 * domestic
        livestock = 0.10 * population * 30

        avg_demand = (domestic + institutional + livestock) / 1_000_000
        max_demand = avg_demand * 1.2 * 1.8

        data.append([year, int(population), round(avg_demand, 3), round(max_demand, 3)])

    df = pd.DataFrame(data, columns=[
        "Year", "Population", "Average Demand (MLD)", "Maximum Demand (MLD)"
    ])

    # Save Excel
    excel_path = "forecast_output.xlsx"
    df.to_excel(excel_path, index=False)

    # Create Graph
    plt.figure()
    plt.plot(df["Year"], df["Average Demand (MLD)"])
    plt.xlabel("Year")
    plt.ylabel("Average Demand (MLD)")
    plt.title("Water Demand Forecast")
    plt.grid(True)
    graph_path = os.path.join("static", "graph.png")
    plt.savefig(graph_path)
    plt.close()

    return render_template("result.html", tables=df.to_html(index=False))

@app.route("/download")
def download():
    return send_file("forecast_output.xlsx", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
