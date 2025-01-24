import os
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder,StandardScaler

class AIManager:
    def __init__(self):
        self.model = None
        self.file_paths = None
        self.le_extension = None
        self.scaler = None

    def extract_features(self, usage_history):
        """
        Extract features from usage history

        Parameters:
            usage_history (list[Tuple[str, str]]): List of tuples containing file paths and timestamps.

        Returns:
            pd.DataFrame: DataFrame containing extracted features.
        """

        data = []
        
        for file_path, timestamp in usage_history:
            timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            hour = timestamp.hour
            weekday = timestamp.weekday()
            extension = self.get_file_extension(file_path)
            data.append({'file_path': file_path, 'hour': hour, 'weekday': weekday, 'extension': extension})

        df = pd.DataFrame(data)
        return df
    
    def get_file_extension(self, file_path):
        _, ext = os.path.splitext(file_path)
        return ext.lower()

    def encode_features(self, df, is_training=False):
        """
        Encode categorical features and normalize numerical features.

        Parameters:
            df (pd.DataFrame): DataFrame containing extracted features.
            is_training (bool): If True, fit the encoders and scalers; otherwise, use existing ones

        Returns:
            np.array: Numpy array of features.
        """

        # Encode 'extension'
        if is_training:
            self.le_extension = LabelEncoder()
            df['extension_encoded'] = self.le_extension.fit_transform(df['extension'])
        else:
            df['extension_encoded'] = self.le_extension.transform(df['extension'])

        # Features
        features = df[['hour', 'weekday', 'extension_encoded']]

        # Normalize features
        if is_training:
            self.scaler = StandardScaler()
            features_scaled = self.scaler.fit_transform(features)
        else:
            features_scaled = self.scaler.transform(features)

        return features_scaled

    def train_model(self, usage_history):
        """
        Train the K-NN model using usage_history.
        """

        if not usage_history:
            print("usage history is empty. Model cannot be trained.")
            self.model = None
            self.file_paths = None
            return

        df = self.extract_features(usage_history)
        features = self.encode_features(df, is_training=True)

        # Store file_paths for later use
        self.file_paths = df['file_path'].reset_index(drop=True)

        # Train K-NN Model
        self.model = NearestNeighbors(n_neighbors=5, algorithm='auto')
        self.model.fit(features)

    def recommend_files(self, current_time):
        """
        Recommend files based on current time.

        Parameters:
            current_time (datetime): Current datetime.

        Returns:
            list[str]: List of recommended file paths.
        """

        if self.model is None or self.file_paths is None or self.le_extension is None or self.scaler is None:
            return []

        hour = current_time.hour
        weekday = current_time.weekday()

        # Assume most common extension for simplicity
        extension = '.pdf'

        # Encoding the features
        input_df = pd.DataFrame([{'hour': hour, 'weekday': weekday, 'extension': extension}])

        # Handle unseen extensions
        if extension not in self.le_extension.classes_:
            input_df['extension'] = 'unknown'

        # Ensure 'unknown' class exists in the encoder
        if 'unknown' not in self.le_extension.classes_:
            self.le_extension.classes_ = np.append(self.le_extension.classes_, 'unknown')

        features_scaled = self.encode_features(input_df, is_training=False)

        distances, indices = self.model.kneighbors(features_scaled)
        recommended_files = self.file_paths.iloc[indices[0]].tolist()

        # Filtering ot files which not exist in system directory
        existing_files = [file for file in recommended_files if os.path.exists(file)]
        return existing_files