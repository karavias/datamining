"""
dm_matlib.

This is module that implements the graphs
needed to display statistics and returns the HTML code to be used
by the web application
"""
import matplotlib.pyplot as plt, mpld3
from dateutil.relativedelta import relativedelta


def generate_pie(data):
    """
    Generate a pie chart with the given data.

    This function receives a list of floats in a range[0,5]
    and generates a pie chart with their distribution in the
    following ranges [0-1], [1-2], [2-3], [3-4], [4-5]

    Keyword arguments:
    data -- a list of numbers from 0 to 5 to give to the pie.
    """
    total = len(data)

    # The slices will be ordered and plotted counter clockwise.
    labels = ['0-1', '1-2', '2-3', '3-4', '4-5']
    cathegories = [0 for i in range(5)]
    for i in range(len(labels)):
        cathegories[i] = len([x for x in data if x > i and x < i+1])

    sizes = []
    for cat in cathegories:
        sizes.append(cat*100/total)
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'cyan']
    explode = (0, 0, 0, 0, 0) # only "explode" the 2nd slice (i.e. 'Hogs')

    #for i in sizes:
        #if i==0:
            #sizes.remove(i)
            #labels.remove()

    # Set aspect ratio to be equal so that pie is drawn as a circle.
    fig, axes = plt.subplots()
    fig.set_size_inches(4, 3)

    axes.pie(sizes, explode=explode, labels=labels, \
        colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    return mpld3.fig_to_html(fig)


def generate_histogram(dates, values):
    """
    Generate a barchart from the given information.

    This function receives a list of floats and a list of labels
    and uses them to generates a barchart histogram.

    Keyword arguments:
    values -- a list of values for each bar of the chart.
    labels -- a list of labels for each bar of the chart.
    """
    #n_groups = len(values)


    fig, axes = plt.subplots()
    axes.plot(dates, values, 'o--')
    plt.ylim([0, 5])
    one_mon_rel = relativedelta(months=1)
    plt.xlim([min(dates), max(dates) + one_mon_rel])
    fig.set_size_inches(12, 5)
    plt.xlabel('Videos through time')
    plt.ylabel('Mean video scores')
    plt.title('Channel\'s video progress through time')
    plt.legend()
    plt.tight_layout()

    return mpld3.fig_to_html(fig)

