# app.py
from shiny import App, ui, render, reactive
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

# --------------------------
# Estaciones
stations = ["ANTENA", "CENTRAL", "RELAVERA", "CHAVIN"]

# --------------------------
# UI
app_ui = ui.page_fluid(
    ui.h2("Dashboard Pronóstico del Tiempo"),
    
    ui.input_select("station_selected", "Selecciona la estación:", {s: s for s in stations}),
    
    ui.br(),

    ui.row(
        ui.column(6, ui.output_plot("plot_precip")),
        ui.column(6, ui.output_plot("plot_tmed"))
    ),
    ui.row(
        ui.column(6, ui.output_plot("plot_tmax")),
        ui.column(6, ui.output_plot("plot_tmin"))
    )
)

# --------------------------
# Server
def server(input, output, session):

    # ⚡ Ahora controlamos con input.station_selected
    @reactive.calc
    def df():
        today = datetime.date.today()
        dates = [today + datetime.timedelta(days=i) for i in range(1, 6)]
        np.random.seed(hash(input.station_selected()) % 2**32)  # genera siempre lo mismo por estación
        return pd.DataFrame({
            "Fecha": dates,
            "Precipitacion (mm)": np.random.uniform(0, 20, 5),
            "Tmed": np.random.uniform(5, 20, 5),
            "Tmax": np.random.uniform(15, 30, 5),
            "Tmin": np.random.uniform(0, 10, 5)
        })

    @output
    @render.plot
    def plot_precip():
        data = df()
        fig, ax = plt.subplots()
        ax.bar(data["Fecha"].astype(str), data["Precipitacion (mm)"])
        ax.set_title(f"Precipitación - {input.station_selected()}")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Precipitación (mm)")
        plt.xticks(rotation=45)
        return fig

    @output
    @render.plot
    def plot_tmed():
        data = df()
        fig, ax = plt.subplots()
        ax.plot(data["Fecha"], data["Tmed"], marker="o")
        ax.set_title(f"Temperatura Media - {input.station_selected()}")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Temperatura Media (°C)")
        plt.xticks(rotation=45)
        return fig

    @output
    @render.plot
    def plot_tmax():
        data = df()
        fig, ax = plt.subplots()
        ax.plot(data["Fecha"], data["Tmax"], marker="o", color="red")
        ax.set_title(f"Temperatura Máxima - {input.station_selected()}")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Temperatura Máxima (°C)")
        plt.xticks(rotation=45)
        return fig

    @output
    @render.plot
    def plot_tmin():
        data = df()
        fig, ax = plt.subplots()
        ax.plot(data["Fecha"], data["Tmin"], marker="o", color="cyan")
        ax.set_title(f"Temperatura Mínima - {input.station_selected()}")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Temperatura Mínima (°C)")
        plt.xticks(rotation=45)
        return fig

# --------------------------
# App
app = App(app_ui, server)
