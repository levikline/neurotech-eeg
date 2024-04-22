# EEG Data Visualization Toolkit

This repository contains a Python module designed for visualizing and comparing EEG (electroencephalography) band power data. The module was created as part of a project for the Neurotech @ Berkeley DeCal.

Data was collected using the Muse2 headset and a forked version of [muse-fft](https://github.com/tanvach/muse-fft).

## Usage

### Dependencies

- `matplotlib`
- `pandas`
- `numpy`
  
You can install these packages using pip:

```console
foo@bar:~$ pip install matplotlib pandas numpy
```

## Quick Start

1. Prepare Your Data: Ensure your EEG data is in JSON format and stored in the appropriate directory (e.g., `data/control.json`). See the "Data Format" section for more details.

2. Load and Plot Data: Use the functions provided to load your data and plot it according to your needs. Example usage is provided in the main section of the script.
   
### Example Scripts

```python
# Load the data from files
data_base = load_data("data/control.json")
data_compare = load_data("data/treatment.json")

# Plot EEG band power for the control dataset
plot_bands(data_base, "Control", ['af7', 'af8', 'tp9', 'tp10'], ['delta', 'theta', 'alpha', 'beta', 'gamma'])

# Compare EEG band power between control and treatment datasets
plot_channel_bands(data_base, data_compare, "Control", "Treatment", "tp9", ['delta', 'theta', 'alpha', 'beta', 'gamma'])
```

## Modules

The script is organized into functions that handle specific types of plots:

- `load_data(file)`: Loads EEG data from a JSON file.
- `plot_bands(data, label, channels, bands)`: Plots the EEG band power for specified channels and bands.
- `plot_channel_bands(data1, data2, data1_label, data2_label, channel, bands)`: Plots EEG band power for a specified channel from two different datasets.
- `plot_band_differences(data1, data2, channels, bands)`: Plots the difference in EEG band power over time for each channel between two datasets.
- `plot_channel_band_ratios(data1, data2, data1_label, data2_label, band1, band2, channels)`: Plots the ratio of two bands over time for each channel between two datasets.

## Data Format

The EEG data used in this toolkit is stored in JSON format, with each file representing a comprehensive collection of EEG readings over a series of time points. Below is a description of the data structure and the format of the collected data.

### Structure

The JSON data is organized as follows:

- Each top-level key represents a time point, indexed numerically (e.g., "0", "1").
- Under each time point, the data is further divided by EEG channel identifiers (e.g., "af8", "af7", "tp9", "tp10").
- Each channel contains measurements for different EEG frequency bands and ratios:
  - delta: Delta wave power
  - theta: Theta wave power
  - alpha: Alpha wave power
  - beta: Beta wave power
  - gamma: Gamma wave power
  - betaThetaRatio: The ratio of beta to theta wave power

### Example Data Point

Below is an example snippet of how the data is formatted for each time point across different channels:

```json
{
  "0": {
    "af8": {
      "delta": 80.33338328679281,
      "theta": 35.82953867251624,
      "alpha": 44.61669149713892,
      "beta": 51.56899170664597,
      "gamma": 67.69530229241505,
      "betaThetaRatio": 1.439287069196986
    },
    "af7": {
      "delta": 4.122490123298392,
      "theta": 2.326828801250914,
      "alpha": 2.2959854519703753,
      "beta": 0.8783128927869157,
      "gamma": 0.48448526564909494,
      "betaThetaRatio": 0.3774720737145469
    },
    "tp9": {
      "delta": 1.5650348313884463,
      "theta": 0.933312513657283,
      "alpha": 0.47618274396033355,
      "beta": 0.8753840507746193,
      "gamma": 0.40844335244636837,
      "betaThetaRatio": 0.9379324052394146
    },
    "tp10": {
      "delta": 65.45186278835067,
      "theta": 33.83912456581516,
      "alpha": 56.65985178425567,
      "beta": 59.07292526715948,
      "gamma": 67.37362572133574,
      "betaThetaRatio": 1.7456989808429002
    }
  }
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

Levi Kline - _Initial work & Maintainer_

Jason Yang - _Initial work_

## Acknowledgments

Members of the OKUltra team (Neurotech @ Berkeley DeCal)
