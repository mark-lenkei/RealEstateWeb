import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime
import pandas as pd
import plotly
import json
import glob


class DataManager:

    def __init__(self, path):
        self.csv_path = glob.glob(path)
        self.df_read = []
        for i in self.csv_path:
            self.df_read.append(pd.read_csv(i))
        self.df = pd.concat([i for i in self.df_read])


    def get_statistics(self, start_date="2022-07-26", end_date=datetime.today().strftime('%Y-%m-%d')):
        if start_date > end_date:
            start_date, end_date = end_date, start_date

        if start_date < self.df.iat[0, 1]:
            start_date = self.df.iat[0, 1]

        if end_date > self.df.iat[-1, 1]:
            end_date = self.df.iat[-1, 1]

        df_time = self.df[(self.df["date"] >= start_date) & (self.df["date"] <= end_date)]
        df_selected = df_time.groupby('date').agg({'price':'median', 'id':'count'})

        def plot(df):
            fig = make_subplots(specs=[[{'secondary_y': True}]])

            fig.add_trace(
                go.Scatter(x=df.index, y=df["price"], name="Median Price"),
                secondary_y=False
            )

            fig.add_trace(
                go.Scatter(x=df.index, y=df["id"], name="Available"),
                secondary_y=True
            )
            
            fig.update_layout(
                title_text = "Median Price vs Available Flats"
            )

            fig.update_xaxes(title_text="Date")
            fig.update_yaxes(title_text="Median Price", secondary_y=False)
            fig.update_yaxes(title_text="Available", secondary_y=True)

            graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

            return graph_json

        def change(df):
            changes = {"available": 0, "price_change": 0}
            df_start = df[df.index == start_date]
            df_end = df[df.index == end_date]
            available = ((df_end["id"].values / df_start["id"].values) - 1) * 100
            price_change = ((df_end["price"].values / df_start["price"].values) - 1) * 100
            changes["available"] = round(available[0].astype(float), 2)
            changes["price_change"] = round(price_change[0].astype(float), 2)
            return changes

        chart = plot(df_selected)
        changes = change(df_selected)
        changes["start_date"] = start_date
        changes["end_date"] = end_date

        return chart, changes



