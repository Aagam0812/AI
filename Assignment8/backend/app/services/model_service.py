from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict, List, Optional
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

class ModelService:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.model_name = "bert-base-uncased"  # Default model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.metrics = {
            "inference_times": [],
            "requests_processed": 0,
            "errors": 0,
            "last_error": None
        }
        self.load_model()

    def load_model(self) -> None:
        """
        Load the model and tokenizer
        """
        try:
            logger.info(f"Loading model: {self.model_name}")
            start_time = time.time()
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.model.to(self.device)
            
            load_time = time.time() - start_time
            logger.info(f"Model loaded successfully in {load_time:.2f} seconds")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            self.metrics["errors"] += 1
            self.metrics["last_error"] = str(e)
            raise

    async def predict(self, text: str) -> Dict:
        """
        Make a prediction using the loaded model
        """
        try:
            start_time = time.time()
            
            # Tokenize input
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            ).to(self.device)

            # Make prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

            # Process results
            prediction_time = time.time() - start_time
            self.metrics["inference_times"].append(prediction_time)
            self.metrics["requests_processed"] += 1

            # Get predicted class and confidence
            predicted_class = torch.argmax(predictions).item()
            confidence = predictions[0][predicted_class].item()

            return {
                "prediction": predicted_class,
                "confidence": confidence,
                "inference_time": prediction_time,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            self.metrics["errors"] += 1
            self.metrics["last_error"] = str(e)
            raise

    def get_metrics(self) -> Dict:
        """
        Get model performance metrics
        """
        avg_inference_time = (
            sum(self.metrics["inference_times"]) / len(self.metrics["inference_times"])
            if self.metrics["inference_times"]
            else 0
        )

        return {
            "model_name": self.model_name,
            "device": self.device,
            "requests_processed": self.metrics["requests_processed"],
            "average_inference_time": avg_inference_time,
            "errors": self.metrics["errors"],
            "last_error": self.metrics["last_error"],
            "timestamp": datetime.now().isoformat()
        }

    def health_check(self) -> Dict:
        """
        Check model health status
        """
        return {
            "status": "healthy" if self.model is not None else "unhealthy",
            "model_loaded": self.model is not None,
            "tokenizer_loaded": self.tokenizer is not None,
            "device": self.device,
            "timestamp": datetime.now().isoformat()
        }
