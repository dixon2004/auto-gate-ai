from controller.vehicle_processor import VehicleDetectionProcessor
from utils.config import VIDEO_SOURCE, MODEL_PATH
from model.predict import PredictDetectionModel
from controller.extract import TextExtraction
from utils.log import write_log
import time
import cv2


model = PredictDetectionModel(MODEL_PATH)
detection = VehicleDetectionProcessor()
extraction = TextExtraction()


def real_time_detection() -> None:
    """
    Run real-time car plate recognition.
    """
    cap = cv2.VideoCapture(VIDEO_SOURCE)

    if not cap.isOpened():
        write_log("error", "Failed to open video capture")
        return

    while True:
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            write_log("error", "Failed to read frame")
            break

        try:
            labels = model.predict(frame)

            for label in labels:
                car_plate = extraction.get_car_plate(frame, label)
                role = detection.verify_vehicle(car_plate)
                if role:
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)

                # Drawing bounding box and label on the frame
                x1, y1 = label["x1"], label["y1"]
                x2, y2 = label["x2"], label["y2"]

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{car_plate} ({role})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            # Calculate and display FPS
            end_time = time.time()
            fps = 1 / (end_time - start_time)
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Show the frame
            cv2.imshow("Detection", frame)

            # Break loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            write_log("error", f"Failed to run car plate recognition: {e}")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    real_time_detection()