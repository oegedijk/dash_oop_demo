from dashboard_components import CovidPlots, CovidDashboard
from dash_bootstrap_components.themes import FLATLY
from dash_oop_components import DashApp

plot_factory = CovidPlots(datafile="covid.csv")
dashboard = CovidDashboard(plot_factory)
app = DashApp(dashboard, external_stylesheets=[FLATLY])
app.to_yaml("dashboard.yaml")






