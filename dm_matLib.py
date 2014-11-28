import numpy as np
import matplotlib.pyplot as plt, mpld3
from mpld3 import plugins
def generate_pie(data):
    total= len(data)

    # The slices will be ordered and plotted counter-clockwise.
    labels = ['0-1','1-2','2-3','3-4','4-5']
    cathegories=[0 for i in range(5)]
    for i in range(len(labels)):
        cathegories[i] = len([x for x in data if x>i and x<i+1 ])

    sizes=[]
    for cat in cathegories:
        sizes.append(cat*100/total)
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','cyan']
    explode = (0, 0, 0, 0,0) # only "explode" the 2nd slice (i.e. 'Hogs')
    """
    for i in sizes:
        if i==0:
            sizes.remove(i)
            labels.remove()
    """
    #fig=plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    fig, ax = plt.subplots()
    fig.set_size_inches(4,3)

    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    plugins.connect(fig, plugins.MousePosition())
    return mpld3.fig_to_html(fig)

def generate_histogram(values, labels):
    n_groups = len(values)
 

    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.1
    
    opacity = 0.4
    fig.set_size_inches(12,5)
    plt.bar(index, values, bar_width,
                     alpha=opacity,
                     color='b',
                     label=labels)
                     
    plt.xlabel('Videos through time')
    plt.ylabel('Mean video scores')
    plt.title('Channel\'s video progress through time')
    plt.xticks(index + bar_width/2, labels)
    plt.legend()
    
    plt.tight_layout()
    plt.ylim([0,5])
  
    plugins.connect(fig, plugins.MousePosition())
    return mpld3.fig_to_html(fig)
#    return mpld3.fig_to_html(fig)
    
