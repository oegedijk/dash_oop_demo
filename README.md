# dash_oop_demo

Deployment example of dash_oop_components library

- `dashboard_components.py` contains the definitions of the `DashFigureFactory` and `DashComponents`
- `build_dashboard.py` builds the `dashboard.yaml` configuration
- `dashboard.py` simply loads the config and exposes the flask app:

```python
from dash_oop_components import DashApp

dashboard = DashApp.from_yaml("dashboard.yaml")
app = dashboard.app.server
```

And then run the dashboard with:

```bash
$ gunicorn dashboard:app
```

