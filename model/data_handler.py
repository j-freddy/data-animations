import os
import sys
import numpy as np
import pandas as pd

from model.const import DIR_IN
from model.feature import Feature
from model.lerp import Lerp

# In general:
# - feature = user
# - entry = day
class DataHandler:
    def __init__(self, filename, num_visible=10):
        self.data = pd.read_csv(os.path.join(DIR_IN, f"{filename}.csv"))
        self.preprocess_data()

        self.num_visible = num_visible

        # Dictionary mapping name to Feature object
        self.features = {
            name: Feature(name, series.values, num_visible)
            for name, series in self.get_features().items()
        }

        # Available units
        base = np.array([1, 2, 5])
        exp_limit = int(np.ceil(np.log10(self.get_max())))

        self.available_units = np.outer(
            np.power(10, np.arange(0, exp_limit)),
            base,
        ).ravel()

        # ================ Perform calculations ================

        # Feature ids of features that are visible per entry
        self.top_features_ids = self.get_top_features_ids()
        # Max feature value per entry
        self.maxes = self.get_maxes()
        # Unit choice per entry
        # Usage: self.available_units[self.units_indices[entry_index]]
        self.units_indices = self.get_units_indices()

        self.update_ranks()
    
    # noqa
    # Specific for largest-cities.csv only
    def preprocess_data(self):
        n, _ = self.data.shape
        ENTRY_PER_YEAR = 30

        # Filter unnecessary columns
        selected_columns = [
            "Year",
            "Urban Agglomeration",
            "Population (millions)",
        ]
        self.data = self.data[selected_columns]

        # Get list of cities
        cities = self.data["Urban Agglomeration"].unique()

        # Construct new DataFrame that fits requirements of this project
        new_data = pd.DataFrame(columns=["Year"] + list(cities))

        entry_index = 0

        for year_index in range(n // ENTRY_PER_YEAR):
            new_data.loc[year_index, "Year"] = self.data.iloc[year_index * ENTRY_PER_YEAR]["Year"]

            for _ in range(ENTRY_PER_YEAR):
                entry = self.data.iloc[entry_index]
                new_data.loc[year_index, entry["Urban Agglomeration"]]\
                    = float(entry["Population (millions)"].replace(" ", ""))
                entry_index += 1
        
        new_data.fillna(0, inplace=True)
        
        self.data = new_data
    
    def num_entries(self):
        return self.get_features().shape[0]

    # Get data without time column
    def get_features(self):
        return self.data.iloc[:, 1:]

    def get_time(self, i):
        return str(self.data.values[i, 0])

    def get_top_features_ids(self):
        return self.get_features().apply(
            lambda entry: entry.nlargest(self.num_visible).index.to_numpy(),
            axis=1,
        )
    
    def get_max(self):
        return self.get_features().max().max()
    
    def get_maxes(self):
        return self.get_features().max(axis=1)

    def get_max_bar_width(self, entry_index: float):
        # TODO Magic numbers
        # 1.15 ensures bar never goes off-screen
        return Lerp.weighted_avg(self.maxes, entry_index, kernel_size=29) * 1.15

    def get_units_indices(self):
        units_indices = np.empty(self.num_entries())

        for i in range(self.num_entries()):
            max_bar_width = self.get_max_bar_width(i)

            # Choose appropriate unit
            min_ticks = 3
            # Choose largest unit that is not too large (i.e. shows at least
            # @min_ticks ticks)
            units_indices[i] = np.where((self.available_units * min_ticks) > max_bar_width)[0][0] - 1
        
        return units_indices
            

    def update_ranks(self):
        for i, entry in enumerate(self.top_features_ids):
            for rank, feature_id in enumerate(entry):
                self.features[feature_id].set_rank(rank, i)
