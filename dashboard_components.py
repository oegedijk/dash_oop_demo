__all__ = ['CovidDashboard']

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_oop_components import DashFigureFactory, DashComponent, DashApp

import pandas as pd
import plotly.express as px


class CovidPlots(DashFigureFactory):
    def __init__(self, datafile="covid.csv", exclude_countries=[]):
        super().__init__()
        self.df = pd.read_csv(datafile)
        if exclude_countries:
            self.df = self.df[~self.df.countriesAndTerritories.isin(exclude_countries)]
        self.countries = self.df.countriesAndTerritories.unique().tolist()
        self.metrics = ['cases', 'deaths']
        
    def plot_time_series(self, countries, metric):
        return px.line(
            data_frame=self.df[self.df.countriesAndTerritories.isin(countries)],
            x='dateRep',
            y=metric,
            color='countriesAndTerritories',
            labels={'countriesAndTerritories':'Countries', 'dateRep':'date'},
            )
    
    def plot_pie_chart(self, countries, metric):
        return px.pie(
            data_frame=self.df[self.df.countriesAndTerritories.isin(countries)],
            names='countriesAndTerritories',
            values=metric,
            hole=.3,
            labels={'countriesAndTerritories':'Countries'}
            ) 

class CovidTimeSeries(DashComponent):
    def __init__(self, plot_factory, 
                 hide_country_dropdown=False, include_countries=None, countries=None, 
                 hide_metric_dropdown=False, include_metrics=None, metric='cases'):
        super().__init__()
        
        if not self.include_countries:
            self.include_countries = self.plot_factory.countries
        if not self.countries:
            self.countries = self.include_countries
        
        if not self.include_metrics:
            self.include_metrics = self.plot_factory.metrics
        if not self.metric:
            self.metric = self.include_metrics[0]
        
    def layout(self):
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H3("Covid Time Series"),
                    self.make_hideable(
                        dcc.Dropdown(
                            id='timeseries-metric-dropdown-'+self.name,
                            options=[{'label': metric, 'value': metric} for metric in self.include_metrics],
                            value=self.metric,
                        ), hide=self.hide_metric_dropdown),
                    self.make_hideable(
                        dcc.Dropdown(
                            id='timeseries-country-dropdown-'+self.name,
                            options=[{'label': country, 'value': country} for country in self.include_countries],
                            value=self.countries,
                            multi=True,
                        ), hide=self.hide_country_dropdown),
                    dcc.Graph(id='timeseries-figure-'+self.name)
                ]),
            ])
        ])
    
    def _register_callbacks(self, app):
        @app.callback(
            Output('timeseries-figure-'+self.name, 'figure'),
            Input('timeseries-country-dropdown-'+self.name, 'value'),
            Input('timeseries-metric-dropdown-'+self.name, 'value')
        )
        def update_timeseries_plot(countries, metric):
            if countries and metric:
                return self.plot_factory.plot_time_series(countries, metric)
            raise PreventUpdate


class CovidPieChart(DashComponent):
    def __init__(self, plot_factory, 
                 hide_country_dropdown=False, include_countries=None, countries=None, 
                 hide_metric_dropdown=False, include_metrics=None, metric='cases'):
        super().__init__()
        
        if not self.include_countries:
            self.include_countries = self.plot_factory.countries
        if not self.countries:
            self.countries = self.include_countries
        
        if not self.include_metrics:
            self.include_metrics = self.plot_factory.metrics
        if not self.metric:
            self.metric = self.include_metrics[0]
        
    def layout(self, params=None):
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H3("Covid Pie Chart"),
                    self.make_hideable(
                        dcc.Dropdown(
                            id='piechart-metric-dropdown-'+self.name,
                            options=[{'label': metric, 'value': metric} for metric in self.include_metrics],
                            value=self.metric,
                        ), hide=self.hide_metric_dropdown),
                    self.make_hideable(
                        dcc.Dropdown(
                            id='piechart-country-dropdown-'+self.name,
                            options=[{'label': country, 'value': country} for country in self.include_countries],
                            value=self.countries,
                            multi=True
                        ), hide=self.hide_country_dropdown),
                    dcc.Graph(id='piechart-figure-'+self.name)
                ]),
            ])
        ])
    
    def _register_callbacks(self, app):
        @app.callback(
            Output('piechart-figure-'+self.name, 'figure'),
            Input('piechart-country-dropdown-'+self.name, 'value'),
            Input('piechart-metric-dropdown-'+self.name, 'value')
        )
        def update_timeseries_plot(countries, metric):
            if countries and metric:
                return self.plot_factory.plot_pie_chart(countries, metric)
            raise PreventUpdate


class CovidComposite(DashComponent):
    def __init__(self, plot_factory, title="Covid Analysis",
                 hide_country_dropdown=False, 
                 include_countries=None, countries=None, 
                 hide_metric_dropdown=False, 
                 include_metrics=None, metric='cases', name=None):
        super().__init__(title=title)
        
        if not self.include_countries:
            self.include_countries = self.plot_factory.countries
        if not self.countries:
            self.countries = self.include_countries
        
        if not self.include_metrics:
            self.include_metrics = self.plot_factory.metrics
        if not self.metric:
            self.metric = self.include_metrics[0]
            
        self.timeseries = CovidTimeSeries(
                plot_factory, 
                hide_country_dropdown=True, countries=self.countries,
                hide_metric_dropdown=True, metric=self.metric)
        
        self.piechart = CovidPieChart(
                plot_factory, 
                hide_country_dropdown=True, countries=self.countries,
                hide_metric_dropdown=True, metric=self.metric)
        
    def layout(self, params=None):
        return dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1(self.title),
                    self.make_hideable(
                        self.querystring(params)(dcc.Dropdown)(
                            id='dashboard-metric-dropdown-'+self.name,
                            options=[{'label': metric, 'value': metric} for metric in self.include_metrics],
                            value=self.metric,
                        ), hide=self.hide_metric_dropdown),
                    self.make_hideable(
                        self.querystring(params)(dcc.Dropdown)(
                            id='dashboard-country-dropdown-'+self.name,
                            options=[{'label': metric, 'value': metric} for metric in self.include_countries],
                            value=self.countries,
                            multi=True,
                        ), hide=self.hide_country_dropdown),
                ], md=6),
            ], justify="center"),
            dbc.Row([
                dbc.Col([
                    self.timeseries.layout(),
                ], md=6),
                dbc.Col([
                    self.piechart.layout(),
                ], md=6)
            ])
        ], fluid=True)
    
    def _register_callbacks(self, app):
        @app.callback(
            Output('timeseries-country-dropdown-'+self.timeseries.name, 'value'),
            Output('piechart-country-dropdown-'+self.piechart.name, 'value'),
            Input('dashboard-country-dropdown-'+self.name, 'value'),
        )
        def update_timeseries_plot(countries):
            return countries, countries
        
        @app.callback(
            Output('timeseries-metric-dropdown-'+self.timeseries.name, 'value'),
            Output('piechart-metric-dropdown-'+self.piechart.name, 'value'),
            Input('dashboard-metric-dropdown-'+self.name, 'value'),
        )
        def update_timeseries_plot(metric):
            return metric, metric


class CovidDashboard(DashComponent):
    def __init__(self, plot_factory, 
                 europe_countries = ['Italy',  'Spain', 'Germany', 'France', 'Iran', 
                                     'United_Kingdom', 'Switzerland', 'Netherlands',  
                                     'Belgium', 'Austria', 'Portugal', 'Norway'],
                asia_countries = ['China', 'Vietnam', 'Malaysia', 'Philippines', 
                                  'Taiwan', 'Myanmar', 'Thailand', 'South_Korea', 'Japan']):
        super().__init__()
        
        self.europe = CovidComposite(self.plot_factory, "Europe", 
                                     include_countries=self.europe_countries, name="eur")
        self.asia = CovidComposite(self.plot_factory, "Asia", 
                                    include_countries=self.asia_countries, name="asia")
        self.cases_only = CovidComposite(self.plot_factory, "Cases Only", 
                                         include_metrics=['cases'], metric='cases',
                                         hide_metric_dropdown=True,
                                         countries=['China', 'Italy', 'Brazil'], name="cases")
        self.deaths_only = CovidComposite(self.plot_factory, "Deaths Only", 
                                          include_metrics=['deaths'], metric='deaths',
                                          hide_metric_dropdown=True,
                                          countries=['China', 'Italy', 'Brazil'], name="deaths")
        
    def layout(self, params=None):
        return dbc.Container([
            dbc.Row([
                html.H1("Covid Dashboard"),
            ]),
            dbc.Row([
                dbc.Col([
                    self.querystring(params)(dcc.Tabs)(id="tabs", value=self.europe.name, 
                        children=[
                            dcc.Tab(label=self.europe.title, 
                                    id=self.europe.name, 
                                    value=self.europe.name,
                                    children=self.europe.layout(params)),
                            dcc.Tab(label=self.asia.title, 
                                    id=self.asia.name, 
                                    value=self.asia.name,
                                    children=self.asia.layout(params)),
                            dcc.Tab(label=self.cases_only.title, 
                                    id=self.cases_only.name, 
                                    value=self.cases_only.name,
                                    children=self.cases_only.layout(params)),
                            dcc.Tab(label=self.deaths_only.title, 
                                    id=self.deaths_only.name, 
                                    value=self.deaths_only.name,
                                    children=self.deaths_only.layout(params)),
                        ]),
                ])
            ])
        ], fluid=True)
    






