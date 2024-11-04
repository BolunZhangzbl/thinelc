# -- Public Imports
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -- Private Imports
from thinelc import PyPBFInt, PyPBFFloat
from thinelc.utils import *


# -- Global Variables


# -- Functions

"""
Bar plots to visualize the distributions of new variables introduction
 against 

1. Number of variables (Unlimited samples)
    e.g., 4, 5, 6, 7, 8, 9, 20, 50, 80, 120
2. Number of variables (30 samples)
3. Number of variables (10 samples)
4. Number of variables (5 samples)
Note: 3 bars for one category on x-axis: 
      mode 0 (ELC+HOCR); mode 1 (ELC Approx); mode 2 (ELC)
"""


def get_newvars_dist(num_vars_list=None, num_samples=None, times_repeat=30):
    # Default list of variable counts if not provided
    num_vars_list = num_vars_list or [4, 5, 6, 7, 8, 9, 20, 50, 80, 120]
    modes = [0, 1, 2]

    results = {}
    print(f"\nRunning on Samples: {num_samples}")
    for num_vars in num_vars_list:
        results[num_vars] = {}

        print(f"Running on Variables: {num_vars}......")
        for mode in modes:
            # Store results for each mode across repeated trials
            newvars_diffs = []

            for _ in range(times_repeat):
                pbf, qpbf = PyPBFInt(), PyPBFInt()
                random_test(pbf, num_vars, 999, -999, sample=num_samples)
                reduce(pbf, qpbf, mode, num_vars)

                # Calculate the difference in variable counts
                num_newvars = qpbf.max_id() - pbf.max_id()
                newvars_diffs.append(num_newvars)

            results[num_vars][mode] = newvars_diffs
    print("Finished !!!")

    return results


def plot_boxplots(data, num_samples=None, save=False):
    """
    Plot box plots with num_vars on the x-axis, num_newvars on the y-axis,
    and each mode (0, 1, 2) represented with different colors.

    Parameters:
    - data: dict, output from get_newvars_dist function with structure:
      {num_vars: {mode: list of num_newvars differences}}
    """
    # Convert the data dictionary to a DataFrame for easy plotting
    records = []
    for num_vars, modes_data in data.items():
        for mode, num_newvars_list in modes_data.items():
            for num_newvars in num_newvars_list:
                records.append({"num_vars": num_vars, "mode": mode, "num_newvars": num_newvars})

    df = pd.DataFrame(records)

    # Set up the plot
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='num_vars', y='num_newvars', hue='mode', data=df, palette='Set2')

    # Add titles and labels
    plt.title("Distribution of num_newvars by num_vars and mode")
    plt.xlabel("num_vars")
    plt.ylabel("num_newvars")

    # Show the legend and plot
    plt.legend(title="Mode")
    plt.tight_layout()

    if save:
        dir_save = r"C:\Users\13580\桌面\24Fall PhD Applications\Research Assistant (Warwick)\ResearchOutputs\Figures_final"
        num_samples = "unlimited" if num_samples is None else num_samples
        file_path_save = os.path.join(dir_save, f"box_newvars_sample_{num_samples}.png")
        plt.savefig(file_path_save, format='png', dpi=300)

    plt.show()

num_samples_list = [100, 50, 30, 10, 5]

for num_samples in num_samples_list:
    d = get_newvars_dist(num_samples=num_samples)
    plot_boxplots(d, num_samples=num_samples, save=True)