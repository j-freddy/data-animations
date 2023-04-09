import math
import numpy as np
import pandas as pd


data = pd.read_csv("data/example.csv")
i = 5
foo = data.values[i, 0]

print(foo)
