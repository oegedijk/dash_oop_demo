from dashboard_components import CovidPlots, CovidDashboard
from dash_bootstrap_components.themes import FLATLY
from dash_oop_components import DashApp

plot_factory = CovidPlots(datafile="covid.csv")
dashboard = CovidDashboard(plot_factory)
dashboard.to_yaml("dashboard_component.yaml")
app = DashApp(dashboard, querystrings=True, bootstrap=FLATLY)
app.to_yaml("dashboard.yaml")






