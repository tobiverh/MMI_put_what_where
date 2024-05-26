import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def load_file(file_name):
    return pd.read_csv(file_name, delimiter=',', header=0)


if __name__ == '__main__':
    time_df = load_file('times.csv')

    # Create the box plot
    plt.figure(figsize=(10, 6))
    box = plt.boxplot(time_df, patch_artist=True,
                      boxprops=dict(facecolor='royalblue', color='black'),
                      medianprops=dict(color='m'),
                      whiskerprops=dict(color='black'),
                      capprops=dict(color='black'))

    # Add labels and title
    plt.ylabel('Time (s)')
    plt.title('Box Plot of Timing Information with Mean and Standard Deviation')

    # Show the plot
    plt.show()
