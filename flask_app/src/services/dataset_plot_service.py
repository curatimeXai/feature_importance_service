import math
import os

import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.services.dataset_service import DatasetService


class DatasetPlotService:
    def __init__(self, data):
        self.data = data
        self.colors = ['#8bdcbe', '#f05a71', '#371ea3', '#EFBD3F', '#C1002A', '#9A001E', '#636363']
        self.dataset_service = DatasetService()

    def create_scatter_plot(self, x, y, xlabel, ylabel):
        plt.figure(figsize=(8, 6))
        plt.scatter(self.data[x], self.data[y], alpha=0.5)
        plt.title(f"{xlabel} vs {ylabel}")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.show()

    def box_plots(self, df, columns, col_count=4, title="Boxplots"):
        fig = make_subplots(rows=math.ceil(len(columns) / col_count), cols=col_count)
        for i, column in enumerate(columns):
            color = self.colors[i % len(self.colors)]
            fig.add_trace(go.Box(y=df[column],
                                 name=self.dataset_service.kaggle_heart_disease_2020_columns[column].get('title',
                                                                                                         column),
                                 marker={'color': color}),
                          row=math.floor(i / col_count) + 1,
                          col=i % col_count + 1)
        fig.update_layout(
            title_text=title,
            font=dict(color='#371ea3'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        return fig

    def pie_charts(self, df, columns, col_count=2, title="Pie Charts", map=None):
        rows = math.ceil(len(columns) / col_count)
        fig = make_subplots(rows=rows, cols=col_count,
                            specs=[[{"type": "pie"} for _ in range(col_count)] for _ in range(rows)])
        for i, column in enumerate(columns):
            value_counts = df[column].value_counts()
            if map is not None:
                value_counts.index = value_counts.index.map(map)
            fig.add_trace(
                go.Pie(labels=value_counts.index, values=value_counts,
                       name=self.dataset_service.kaggle_heart_disease_2020_columns[column].get('title',
                                                                                               column),
                       marker=dict(colors=self.colors),
                       title=self.dataset_service.kaggle_heart_disease_2020_columns[column].get('title',
                                                                                                column)),
                row=math.floor(i / col_count) + 1,
                col=i % col_count + 1)
        fig.update_traces(hoverinfo='label+percent+name', textinfo='none')
        fig.update_layout(
            title_text=title,
            font=dict(color='#371ea3'),
            margin=dict(t=40, b=0, l=0, r=0)
        )
        return fig

    def plot_a_and_b(self, col):
        unique_vals = self.data[col].unique()
        unique_vals.sort()
        probs = []
        for unique_val in unique_vals:
            count_heart_dis = self.data[self.data[col] == unique_val]["HeartDisease"].count()
            probs.append(count_heart_dis / self.data.shape[0])

        plt.plot(unique_vals, probs, marker='o', linestyle='-')
        plt.show()

    def plot_a_given_b(self, col):
        groups = self.data.groupby([col])
        probabilities = groups['HeartDisease'].mean()
        plt.plot(probabilities.index, probabilities.values, marker='o', linestyle='-')
        plt.title(f"HeartDisease given {col}")
        plt.show()

    def plot_distribution(self, col):
        distribution = self.data[col].value_counts()
        zipped = list(zip(distribution.index, distribution.values))
        zipped_sorted = sorted(zipped, key=lambda x: x[0])
        x_values = [item[0] for item in zipped_sorted]
        y_values = [item[1] for item in zipped_sorted]

        # Plotting the distribution as a bar plot
        plt.plot(x_values, y_values, marker='o', linestyle='-')
        plt.title(f"Distribution of {col}")
        plt.show()
