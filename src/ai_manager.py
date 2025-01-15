import os
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder,StandardScaler

class AIManager:
    def __init__(self):
        self.model = None
        self.file_features = None

    

    def recommend_files(self, usage_history):
        """
        Return recommended files based on usage history.

        Parameters:
            usage_history (List[str]): List of file paths from usage history.

        Returns:
            List[str]: List of recommended file paths.
        """

        file_counter = {}
        for file in usage_history:
            if file in file_counter:
                file_counter[file] += 1
            else:
                file_counter[file] = 1

        # Sorting files by usage frequency
        sorted_files = sorted(file_counter.items(), key=lambda x: x[1], reverse=True)
        recommendedations = [file[0] for file in sorted_files[:10]]

        return recommendedations