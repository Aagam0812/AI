import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from sklearn.model_selection import train_test_split
import logging
from datetime import datetime
import json
import os

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.raw_data_path = os.path.join(data_dir, "raw")
        self.processed_data_path = os.path.join(data_dir, "processed")
        self.metadata = {
            "last_processed": None,
            "total_samples": 0,
            "data_quality_metrics": {},
            "preprocessing_steps": []
        }
        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.raw_data_path, exist_ok=True)
        os.makedirs(self.processed_data_path, exist_ok=True)

    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Load data from various file formats
        """
        try:
            file_extension = file_path.split('.')[-1].lower()
            if file_extension == 'csv':
                data = pd.read_csv(file_path)
            elif file_extension == 'json':
                data = pd.read_json(file_path)
            elif file_extension in ['xls', 'xlsx']:
                data = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
            
            logger.info(f"Successfully loaded data from {file_path}")
            return data
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

    def validate_data(self, data: pd.DataFrame) -> Dict:
        """
        Perform data validation and quality checks
        """
        quality_metrics = {
            "total_rows": len(data),
            "missing_values": data.isnull().sum().to_dict(),
            "duplicates": data.duplicated().sum(),
            "data_types": data.dtypes.astype(str).to_dict()
        }

        # Calculate basic statistics for numerical columns
        numerical_cols = data.select_dtypes(include=[np.number]).columns
        if len(numerical_cols) > 0:
            quality_metrics["numerical_statistics"] = {
                col: {
                    "mean": data[col].mean(),
                    "std": data[col].std(),
                    "min": data[col].min(),
                    "max": data[col].max()
                } for col in numerical_cols
            }

        return quality_metrics

    def preprocess_data(self, data: pd.DataFrame, config: Dict) -> Tuple[pd.DataFrame, Dict]:
        """
        Preprocess data according to configuration
        """
        processed_data = data.copy()
        preprocessing_steps = []

        try:
            # Handle missing values
            if config.get("handle_missing", True):
                for col in processed_data.columns:
                    if processed_data[col].isnull().any():
                        if processed_data[col].dtype in [np.number]:
                            processed_data[col].fillna(processed_data[col].mean(), inplace=True)
                            preprocessing_steps.append(f"Filled missing values in {col} with mean")
                        else:
                            processed_data[col].fillna(processed_data[col].mode()[0], inplace=True)
                            preprocessing_steps.append(f"Filled missing values in {col} with mode")

            # Remove duplicates
            if config.get("remove_duplicates", True):
                initial_rows = len(processed_data)
                processed_data.drop_duplicates(inplace=True)
                removed_rows = initial_rows - len(processed_data)
                preprocessing_steps.append(f"Removed {removed_rows} duplicate rows")

            # Feature scaling (if specified)
            if config.get("scale_features", False):
                from sklearn.preprocessing import StandardScaler
                numerical_cols = processed_data.select_dtypes(include=[np.number]).columns
                if len(numerical_cols) > 0:
                    scaler = StandardScaler()
                    processed_data[numerical_cols] = scaler.fit_transform(processed_data[numerical_cols])
                    preprocessing_steps.append(f"Applied StandardScaler to numerical columns")

            # Update metadata
            self.metadata.update({
                "last_processed": datetime.now().isoformat(),
                "total_samples": len(processed_data),
                "preprocessing_steps": preprocessing_steps
            })

            return processed_data, self.metadata

        except Exception as e:
            logger.error(f"Error during preprocessing: {str(e)}")
            raise

    def split_data(self, data: pd.DataFrame, test_size: float = 0.2, 
                   validation_size: float = 0.1) -> Dict[str, pd.DataFrame]:
        """
        Split data into train, validation, and test sets
        """
        try:
            # First split: separate test set
            train_val, test = train_test_split(data, test_size=test_size, random_state=42)
            
            # Second split: separate validation set from training set
            if validation_size > 0:
                val_size = validation_size / (1 - test_size)
                train, val = train_test_split(train_val, test_size=val_size, random_state=42)
                return {
                    "train": train,
                    "validation": val,
                    "test": test
                }
            else:
                return {
                    "train": train_val,
                    "test": test
                }

        except Exception as e:
            logger.error(f"Error splitting data: {str(e)}")
            raise

    def save_processed_data(self, data: pd.DataFrame, filename: str):
        """
        Save processed data with metadata
        """
        try:
            # Save processed data
            output_path = os.path.join(self.processed_data_path, filename)
            data.to_csv(output_path, index=False)
            
            # Save metadata
            metadata_path = os.path.join(self.processed_data_path, f"{filename}_metadata.json")
            with open(metadata_path, 'w') as f:
                json.dump(self.metadata, f, indent=2)
            
            logger.info(f"Saved processed data to {output_path}")
            logger.info(f"Saved metadata to {metadata_path}")

        except Exception as e:
            logger.error(f"Error saving processed data: {str(e)}")
            raise

    def get_processing_status(self) -> Dict:
        """
        Get current data processing status and metadata
        """
        return {
            "metadata": self.metadata,
            "data_directory": self.data_dir,
            "available_files": {
                "raw": os.listdir(self.raw_data_path) if os.path.exists(self.raw_data_path) else [],
                "processed": os.listdir(self.processed_data_path) if os.path.exists(self.processed_data_path) else []
            }
        }
