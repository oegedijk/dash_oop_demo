from dash_oop_components import DashApp

dashboard = DashApp.from_yaml("dashboard.yaml")
app = dashboard.app.server