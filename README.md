# dash_oop_demo

Deployment example of dash_oop_components library

- `dashboard_components.py` contains the definitions of the `DashFigureFactory` and `DashComponents`
- `build_dashboard.py` builds the `dashboard.yaml` configuration:

```python
from dashboard_components import CovidPlots, CovidDashboard
from dash_bootstrap_components.themes import FLATLY
from dash_oop_components import DashApp

plot_factory = CovidPlots(datafile="covid.csv")
dashboard = CovidDashboard(plot_factory)
app = DashApp(dashboard, external_stylesheets=[FLATLY])
app.to_yaml("dashboard.yaml")
```

- `dashboard.py` simply loads the config and exposes the flask app:

```python
from dash_oop_components import DashApp

dashboard = DashApp.from_yaml("dashboard.yaml")
app = dashboard.app.server
```

And then run the dashboard with:

```bash
$ gunicorn --preload dashboard:app
```

