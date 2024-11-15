import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_plots(data):
    df = pd.DataFrame(data)
    fig1 = generate_pie_chart(df, 'Pclass', 'Fare')
    fig2 = generate_scatter_plot(df, 'Age', 'Fare')
    fig3 = generate_box_plot(df, 'Pclass', 'Fare')
    fig4 = generate_box_plot(df, 'Pclass', 'Age')

    # Save the figures to buffers and return them
    img_buffers = []
    for fig in [fig1, fig2, fig3, fig4]:
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        img_buffers.append(img_buffer)

    return img_buffers

def generate_pie_chart(df, col1, col2):
    # Sum the values by the specified columns and plot a pie chart
    group = df.groupby(col1)[col2].sum()
    fig, ax = plt.subplots()
    group.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90)
    ax.set_ylabel('')
    return fig

def generate_scatter_plot(df, col1, col2):
    fig, ax = plt.subplots()
    ax.scatter(df[col1], df[col2], alpha=0.5)
    ax.set_xlabel(col1)
    ax.set_ylabel(col2)
    return fig

def generate_box_plot(df, col1, col2):
    fig, ax = plt.subplots()
    df.boxplot(column=col2, by=col1, ax=ax)
    ax.set_xlabel(col1)
    ax.set_ylabel(col2)
    plt.suptitle('')  # Remove the extra title added by pandas' boxplot
    return fig
