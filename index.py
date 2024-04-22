__author__ = "Levi Kline, Jason Yang"
__copyright__ = "Copyright 2024"
__credits__ = ["Members of the OKUltra team (Neurotech @ Berkeley DeCal)"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Levi Kline"
__email__ = "levibkline@berkeley.edu"

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

DEFAULT_CHANNELS = ['af7', 'af8', 'tp9', 'tp10']
DEFAULT_BANDS = ['delta', 'theta', 'alpha', 'beta', 'gamma']
COLORS = ['deepskyblue', 'orangered', 'orange', 'yellowgreen']

#############################################
### Functions ###
#############################################

def load_data(file):
    '''
    Load the data from the specified file.
    '''
    data = pd.read_json(file)
    return data

def plot_bands(data, title, channels = DEFAULT_CHANNELS, bands = DEFAULT_BANDS):
    '''
    Plot the EEG band power over time for each channel for a given dataset.
    '''    
    # Initialize the subplots
    fig, axs = plt.subplots(len(bands), 1, figsize=(15, 10), sharex=True)
    fig.suptitle('EEG Band Power over Time ({})'.format(title))

    # Define the X-axis values
    data_x_values = [i for i in range(data.shape[1])]
    
    # Plot the data for each band
    for index, band in enumerate(bands):
        data_y_values = [] # Y-axis values for each channel

        # Gather data for each channel within the band
        for row in data.iterrows():
            # Skip the channel if it does not match the specified channels
            if row[0] not in channels:
                continue

            channel_y_values = [] # Y-axis values for the current channel

            # Append the band power value for each time point
            for i in range(data.shape[1]):
                channel_y_values.append(row[1][i][band])

            data_y_values.append(channel_y_values)

        # Plot the data for each channel
        for i in range(len(channels)):
            axs[index].plot(data_x_values, data_y_values[i], color=COLORS[i])

        # Set the plot properties
        axs[index].set_title(band)
        axs[index].set_ylabel('Power')
        axs[index].legend(channels)
        
        # Calculate the upper bound based on the y values
        y_values = np.concatenate(data_y_values)  # Flatten the array of arrays
        upper_bound = np.percentile(y_values, 95)  # Exclude top 5% outliers
        axs[index].set_ylim(0, upper_bound)

    plt.show()

def plot_channel_bands(data1, data2, channel = DEFAULT_CHANNELS[0], bands = DEFAULT_BANDS):
    '''
    Plot the EEG band power over time for a channel from two datasets on the same axes for comparison.
    '''
    # Initialize the subplots
    fig, axs = plt.subplots(len(bands), 1, figsize=(15, 10), sharex=True)
    fig.suptitle('EEG Band Power over Time ({})'.format(channel.capitalize()))

    # Define the X-axis values based on the shortest dataset
    num_time_points = min(data1.shape[1], data2.shape[1])
    data_x_values = [i for i in range(num_time_points)]

    # Plot the data for each band
    for index, band in enumerate(bands):
        data1_y_values = []  # Y-axis values for data1
        data2_y_values = []  # Y-axis values for data2

        # Gather the data for the channel within the band for the first dataset
        for row in data1.iterrows():
            # Skip the channel if it does not match the specified channel
            if row[0] != channel:
                continue

            for i in range(num_time_points):
                data1_y_values.append(row[1][i][band])

        # Gather the data for the channel within the band for the second dataset
        for row in data2.iterrows():
            # Skip the channel if it does not match the specified channel
            if row[0] != channel:
                continue

            for i in range(num_time_points):
                data2_y_values.append(row[1][i][band])
        
        # Plot the data for the channel
        axs[index].plot(data_x_values, data1_y_values, color=COLORS[0])
        axs[index].plot(data_x_values, data2_y_values, color=COLORS[1])

        # Set the plot properties
        axs[index].set_title(band)
        axs[index].set_ylabel('Power')
        axs[index].legend(['Dataset 1', 'Dataset 2'])

        # Calculate the upper bound for Y-axis
        y_values = np.array(data1_y_values + data2_y_values)
        upper_bound = np.percentile(y_values, 95)  # Exclude top 5% outliers
        axs[index].set_ylim(0, upper_bound)

    plt.show()

def plot_band_differences(data1, data2, channels = DEFAULT_CHANNELS, bands = DEFAULT_BANDS):
    '''
    Plot the difference in EEG band power over time for each channel between two datasets.
    '''
    # Initialize the subplots
    fig, axs = plt.subplots(len(bands), 1, figsize=(15, 10), sharex=True)
    fig.suptitle('Difference in EEG Band Power over Time')

    # Define the X-axis values
    num_time_points = min(data1.shape[1], data2.shape[1])
    data_x_values = [i for i in range(num_time_points)]
        
    # Plot the data for each band
    for index, band in enumerate(bands):
        data1_band_values = [] # Band values for data1
        data2_band_values = [] # Band values for data2
        
        # Gather data for each channel within the band from the first dataset
        for row in data1.iterrows():
            # Skip the channel if it does not match the specified channels
            if row[0] not in channels:
                continue

            row_values = [] # Y-axis values for the current channel

            # Append the band power value for each time point
            for i in range(num_time_points):
                row_values.append(row[1][i][band])

            data1_band_values.append(row_values)

        # Gather data for each channel within the band from the second dataset
        for row in data2.iterrows():
            # Skip the channel if it does not match the specified channels
            if row[0] not in channels:
                continue

            row_values = [] # Y-axis values for the current channel

            # Append the band power value for each time point
            for i in range(num_time_points):
                row_values.append(row[1][i][band])

            data2_band_values.append(row_values)
                
        # Calculate the differences and plot
        differences = np.subtract(data2_band_values, data1_band_values) # data2 - data1
        for i in range(len(channels)):
            axs[index].plot(data_x_values, differences[i], color=COLORS[i], label=channels[i])
        
        # Set the plot properties
        axs[index].set_title(band)
        axs[index].set_ylabel('Power Difference')
        axs[index].legend(channels)
        
        # Calculate the upper and lower bound based on the y values
        y_values = np.concatenate(differences)
        upper_bound = np.percentile(y_values, 95) # Exclude top 5% outliers
        lower_bound = np.percentile(y_values, 5) # Exclude bottom 5% outliers
        axs[index].set_ylim(lower_bound, upper_bound)

    plt.show()

def plot_channel_band_ratios(data1, data2, band1="beta", band2="theta", channels=DEFAULT_CHANNELS):
    '''
    Plot the ratio of two bands over time for each channel between two datasets.
    '''
    # Initialize the subplots
    fig, axs = plt.subplots(len(channels), 1, figsize=(15, 10), sharex=True)
    fig.suptitle('Channel {} over Time'.format(band1.capitalize() + '/' + band2.capitalize()))

    # Define the X-axis values
    num_time_points = min(data1.shape[1], data2.shape[1])
    data_x_values = [i for i in range(num_time_points)]

    # Calculate the beta/theta ratios for each channel in the first dataset
    data1_ratio_values = []
    for row in data1.iterrows():
        # Skip the channel if it does not match the specified channels
        if row[0] not in channels:
            continue

        row_values = [] # Y-axis values for the current channel

        # Append the beta/theta ratio for each time point
        for i in range(num_time_points):
            row_values.append(row[1][i][band1] / row[1][i][band2])

        data1_ratio_values.append(row_values)

    # Calculate the beta/theta ratios for each channel in the second dataset
    data2_ratio_values = []
    for row in data2.iterrows():
        # Skip the channel if it does not match the specified channels
        if row[0] not in channels:
            continue

        row_values = [] # Y-axis values for the current channel

        # Append the beta/theta ratio for each time point
        for i in range(num_time_points):
            row_values.append(row[1][i][band1] / row[1][i][band2])

        data2_ratio_values.append(row_values)

    # Plot the beta/theta ratios for each channel
    for i in range(len(channels)):
        axs[i].plot(data_x_values, data1_ratio_values[i], color=COLORS[0])
        axs[i].plot(data_x_values, data2_ratio_values[i], color=COLORS[1])

        # Set the plot properties
        axs[i].set_title(channels[i])
        axs[i].set_ylabel('Ratio')
        axs[i].legend(['Dataset 1', 'Dataset 2'])

        # Calculate the upper and lower bound based on the y values
        y_values = np.array(data1_ratio_values[i] + data2_ratio_values[i])
        upper_bound = np.percentile(y_values, 95) # Exclude top 5% outliers
        lower_bound = np.percentile(y_values, 5) # Exclude bottom 5% outliers
        axs[i].set_ylim(lower_bound, upper_bound)

    plt.show()

#############################################
### Main ###
#############################################

# Available files:
# - control.json
# - control-alt.json
# - treatment.json

# Load the data from the files
data_base = load_data("control.json")
data_compare = load_data("treatment.json")

# Define the channels and bands to plot
#
# You can set these values to DEFAULT_CHANNELS and DEFAULT_BANDS to use the
# default values or change them to plot different channels and bands.
channels = ['af7', 'af8', 'tp9', 'tp10']
bands = ['delta', 'theta', 'alpha', 'beta', 'gamma']

# Call the functions below to plot the data as needed; Each plot will open in a
# new window after the previous one is closed.

plot_bands(data_base, "Control", channels, bands)
plot_bands(data_compare, "Treatment", channels, bands)
plot_channel_bands(data_base, data_compare, "tp9", bands)
plot_band_differences(data_base, data_compare, channels, bands)
plot_channel_band_ratios(data_base, data_compare, "beta", "theta", channels)
