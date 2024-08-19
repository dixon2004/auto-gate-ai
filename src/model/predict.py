from src.utils.log import write_log
from ultralytics import YOLO
import torch


class PredictDetectionModel:

    def __init__(self, model, save=False) -> None:
        """
        Initialize the YOLO model for prediction.
        """
        self.best_model = YOLO(model)
        self.save = save
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


    def check_overlap(self, coordinate_1: dict, coordinate_2: dict) -> bool:
        """
        Check if two bouding boxes overlap.

        Args:
            coordinate_1 (dict): The first bounding box.
            coordinate_2 (dict): The second bounding box.

        Returns:
            bool: True if the bounding boxes overlap, False otherwise.
        """
        try:
            x_left = max(coordinate_1["x1"], coordinate_2["x1"])
            y_top = max(coordinate_1["y1"], coordinate_2["y1"])
            x_right = min(coordinate_1["x2"], coordinate_2["x2"])
            y_bottom = min(coordinate_1["y2"], coordinate_2["y2"])

            if x_right < x_left or y_bottom < y_top:
                return False

            intersection_area = (x_right - x_left) * (y_bottom - y_top)
            coordinate_1_area = (coordinate_1["x2"] - coordinate_1["x1"]) * (coordinate_1["y2"] - coordinate_1["y1"])
            coordinate_2_area = (coordinate_2["x2"] - coordinate_2["x1"]) * (coordinate_2["y2"] - coordinate_2["y1"])
            union_area = coordinate_1_area + coordinate_2_area - intersection_area

            iou = intersection_area / union_area
            return iou > 0.3
        
        except Exception as e:
            write_log("error", f"[PredictDetectionModel] Failed to check overlap: {e}")


    def filter_nms(self, label: list) -> list:
        """
        Filter double detection using Non-Maximum Suppression (NMS).
        
        Args:
            label (list): The list of labels to filter.
            
        Returns:
            list: The list of labels after filtering.
        """
        try:
            for coord_1 in label:
                for coord_2 in label:
                    if coord_1 != coord_2:
                        if self.check_overlap(coord_1, coord_2):
                            if coord_1["confidence"] > coord_2["confidence"]:
                                label.remove(coord_2)
                            else:
                                label.remove(coord_1)

            return label
        
        except Exception as e:
            write_log("error", f"[PredictDetectionModel] Failed to filter NMS: {e}")


    def get_label(self, results: list) -> dict:
        """
        Extract the label from the results.
        
        Args:
            results (list): The results from the prediction.
        
        Returns:
            dict: The label extracted from the results.
        """
        try:
            detection = []

            for result in results:
                for box in result.boxes:
                    label = {}
                    label["x1"] = int(box.xyxy[0][0].item())
                    label["y1"] = int(box.xyxy[0][1].item())
                    label["x2"] = int(box.xyxy[0][2].item())
                    label["y2"] = int(box.xyxy[0][3].item())
                    label["confidence"] = box.conf.item()
                    label["class_id"] = box.id
                    detection.append(label)

            return detection
        
        except Exception as e:
            write_log("error", f"[PredictDetectionModel] Failed to extract label: {e}")    


    def predict(self, src: str) -> dict:
        """
        Run object detection on the image.
        
        Args:
            src (str): The source to the image.
            
        Returns:
            dict: The label extracted from the image.
        """
        try:
            results = self.best_model.predict(
                                    source=src, 
                                    conf=0.25, 
                                    iou=0.7,
                                    device=self.device,
                                    save=self.save,
                                    save_txt=self.save,
                                    save_conf=self.save
                                    )
            
            label = self.get_label(results)
            filtered_label = self.filter_nms(label)
            return filtered_label
        
        except Exception as e:
            write_log("error", f"[PredictDetectionModel] Failed to predict: {e}")
