import matplotlib.pyplot as plt

def bar_plot(df, column):
    fig, ax = plt.subplots()
    df[column].value_counts().plot(kind="bar", ax=ax)
    ax.set_title(f"Bar chart of {column}")
    return fig
