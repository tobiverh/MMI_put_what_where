import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_rel

ALPHA = 0.05


def load_file(file_name):
    return pd.read_csv(file_name, delimiter=',', header=0)


if __name__ == '__main__':
    word_names = ['go_back', 'pick_up', 'collect', 'delete', 'new_object', 'release', 'select']
    word_accuracies = []
    word_ttests = []
    run_1 = []
    run_2 = []
    for word_name in word_names:
        word_df = load_file(word_name + '.csv')
        run_1.append(word_df.get('run_1'))
        run_2.append(word_df.get('run_2'))
        word_ttests.append((word_name, ttest_rel(word_df.get('run_1'), word_df.get('run_2'), alternative='less')))
        word_accuracies.append([np.mean(word_df.get('run_1')), np.mean(word_df.get('run_2'))])

    r1_mean = np.array(np.mean([r1.values for r1 in run_1], axis=0))
    r2_mean = np.array(np.mean([r2.values for r2 in run_2], axis=0))
    word_ttests.append(['average', ttest_rel(r1_mean, r2_mean, alternative='less')])
    word_accuracies.append([np.mean(r1_mean), np.mean(r2_mean)])

    word_accuracies = np.array(word_accuracies)
    print(word_accuracies[:, 0])

    # print(word_ttests[0][1].pvalue)
    # exit(0)

    # Extract the first and second values
    first_values = [pair[0] for pair in word_accuracies]
    second_values = [pair[1] for pair in word_accuracies]

    # Create an array of indices for the x-axis
    indices = np.arange(len(word_accuracies))

    # Width of the bars
    width = 0.35

    # Create the bar plot
    plt.figure(figsize=(12, 6))

    # Plot the bars for the first values
    bars1 = plt.bar(indices - width / 2, first_values, width, label='No Audio Correction', color='lightsteelblue')

    # Plot the bars for the second values
    bars2 = plt.bar(indices + width / 2, second_values, width, label='Audio Correction', color='royalblue')

    # Add labels and title
    plt.xlabel('Word Tested')
    plt.ylabel('Accuracy')
    plt.title('Paired Accuracy T-Test Results')
    plt.xticks(indices, word_names + ['average'])  # Set x-ticks to be at the indices
    plt.legend(loc='upper right')
    plt.grid(axis='y')

    # Add significance indicators
    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        p_val = word_ttests[i][1].pvalue
        if p_val < ALPHA:
            # Get the height of the bars
            height1 = bar1.get_height()
            height2 = bar2.get_height()

            # Calculate the position for the indicator
            max_height = max(height1, height2)

            # Draw the line
            plt.plot([bar1.get_x() + bar1.get_width() / 2.0, bar2.get_x() + bar2.get_width() / 2.0],
                     [max_height, max_height], color='black', linewidth=1.5)

            if p_val < 0.00005:
                char = '***'
            elif p_val < 0.001:
                char = '**'
            else:
                char = '*'
            # Draw the significance indicator
            plt.text((bar1.get_x() + bar2.get_x()) / 2.0 + bar1.get_width() / 2.0, max_height,
                     char, ha='center', va='bottom', color='black', fontsize=14)

    # Show the plot
    plt.show()
