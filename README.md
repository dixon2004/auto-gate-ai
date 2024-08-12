# AutoGate AI

## Project Overview
<p align="justify">
<strong>AutoGate AI</strong> is a cutting-edge automated gate control system, meticulously designed to enhance security and streamline access management for various secured environments, including gated communities, residential complexes, and high-security facilities. Specially tailored for vehicle access in Malaysia, the system is versatile enough to be deployed at both entry and exit points, offering comprehensive monitoring and control over vehicle access.

The system employs advanced artificial intelligence techniques to manage vehicle access effectively. Real-time video feeds from strategically positioned cameras are processed to detect vehicle license plates using the YOLOv10 object detection model. The detected plate numbers are then accurately extracted using EasyOCR for text recognition. This extracted data is cross-referenced with a centralized MongoDB database to determine access permissions.

In addition to its core access control functionalities, <strong>AutoGate AI</strong> includes a user-friendly web interface developed with Python Flask. This interface empowers users to efficiently manage visitor and resident records, as well as review historical access logs. The system is engineered for high accuracy and reliability, incorporating Non-Maximum Suppression (NMS) to handle multiple detections and minimize false positives.
</p>

## Table of Contents
- [Project Overview](#project-overview)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Set Up a Virtual Environment](#set-up-a-virtual-environment)
  - [Install Dependencies](#install-dependencies)
  - [Configure Environment Variables](#configure-environment-variables)
  - [Running the System](#running-the-system)
  - [Running the Web Interface](#running-the-web-interface)
- [Usage](#usage)
  - [AutoGate AI System](#autogate-ai-system)
  - [Web Interface](#web-interface)
- [Showcase](#showcase)
  - [AutoGate AI System](#autogate-ai-system-1)
  - [Web Interface](#web-interface-1)
- [License](#license)

## Setup Instructions

### Prerequisites

- **Python 3.8+**: Required to run the system.
- **MongoDB**: Ensure MongoDB is installed and configured.

  - **[MongoDB Installation Guide](https://docs.mongodb.com/manual/installation/)**: Follow this guide to install MongoDB on your local machine.
  - **[Free MongoDB Atlas](https://www.mongodb.com/cloud/atlas)**: Consider a free cloud-hosted MongoDB instance if you prefer not to run MongoDB locally.

### Clone the Repository
First, clone the repository:
```bash
git clone https://github.com/dixonloke/auto-gate-ai.git
cd auto-gate-ai
```

### Set Up a Virtual Environment
It is recommended to use Python 3.10 to create the virtual environment. Follow these steps:

1.	Create a virtual environment:
```bash
python3.10 -m venv venv  # Preferably use Python 3.10
```

2. Activate the virtual environment:
- **On Windows:**
```bash
venv\Scripts\activate
```
- **On macOS/Linux:**
```bash
source venv/bin/activate
```

### Install Dependencies
With the virtual environment activated, install the necessary dependencies:
```bash
pip install -r requirements.txt
```

### Configure Environment Variables
Before running the system, you must configure the environment variables. A template.env file is included in the project. Here’s how to set it up:

1. Open the `template.env` file located in the project root directory.
2. Fill in the appropriate values for each variable as described in the table below:

| Variable             | Description                                                | Default Value                  |
|----------------------|------------------------------------------------------------|--------------------------------|
| `DATABASE_URL`       | Connection string for your MongoDB instance               | `mongodb://localhost:27017`    |
| `MODEL_PATH`         | Path to the YOLOv10 model file                             | `./yolo_model/best.pt` (Default)|
| `VIDEO_SOURCE`       | Source for capturing real-time video; specify `0` for the default camera or a different index for other cameras | `0`                            |
| `ACTION_OPTION`      | Action option, such as "entry" or "exit"                   | `entry`                        |
| `ADMIN_PHONE_NUMBER` | Phone number for admin notifications                       | `60123456789`                  |
| `ADMIN_PASSWORD`     | Password for the admin interface                           | `securepassword`               |

**Note:** The `ADMIN_PHONE_NUMBER` and `ADMIN_PASSWORD` are critical for logging into the web interface. Keep them secure, as they grant full access to the system.

3.	Rename `template.env` to `.env`, ensuring that it starts with a dot (.).

### Running the System
To start the AutoGate AI system, run the following command:
```bash
python src/main.py
```

### Running the Web Interface
To start the web interface, run the following command:
```bash
python src/view/app.py
```
The web interface starts on port 8000 by default. If this port is in use, the application will automatically find and use the next available port. Once running, you can access the interface via your web browser at the specified URL (typically http://127.0.0.1:8000/ or the next available port).

**Note**: The system and web interface can operate on separate devices if necessary. Ensure both devices are connected to the same and correct database instance. The web interface will communicate with the system remotely, offering flexible deployment options.

## Usage

### AutoGate AI System
The AutoGate AI system automates vehicle access control by processing real-time video feeds to detect and validate vehicle license plates. Here’s a step-by-step overview of how the system operates:

1.	**Car Approaches the Gate:**
- As a vehicle approaches the gate, the system captures live video footage using a connected camera.

3.	**License Plate Detection:**
- The system utilizes the YOLOv10 object detection model to identify the vehicle’s license plate within the video stream.

4. **Text Extraction:**
- Once the license plate is detected, EasyOCR is employed to extract the text from the plate, converting the image of the license plate into a string of characters.

5.	**Database Verification:**
- The extracted license plate number is then cross-referenced with the records stored in the MongoDB database. The system checks whether the vehicle is registered as a resident, a visitor, or if it has any specific access permissions.

6.	**Access Decision:**
- Based on the database check, the system makes an automated decision:
  -	If the plate number is found and validated according to the rules, the system displays the user’s role (e.g., resident, visitor) along with the license plate number, and the gate opens automatically, granting access.
  -	If the plate number is not recognized or is flagged, the system displays the license plate number with “unknown” as the user role, and the gate remains closed.

This process ensures secure and efficient management of vehicle access, minimizing human intervention while maximizing accuracy.

### Web Interface
The AutoGate AI system includes a user-friendly web interface designed to provide comprehensive control and monitoring capabilities. Through this interface, users can perform various administrative tasks:

1.	**Manage Records:**
-	Administrators have the ability to add, remove, and update records for both residents and visitors. This ensures that the system has the most current access information in real-time.
-	Residents are empowered to manage their visitor records by adding or removing visitor entries as needed, offering flexibility and control over who can access the premises.
2.	**View Access History:**
-	The web interface provides a detailed log of all vehicle entries and exits, complete with timestamps, license plate numbers, user roles, and access decisions. This historical data can be used for auditing, security reviews, or troubleshooting.
3.	**User-Friendly Dashboard:**
- The dashboard offers an intuitive layout where administrators can quickly view system status, recent activity, and perform actions without needing deep technical knowledge.

## Showcase

### AutoGate AI System

The AutoGate AI system provides a seamless experience for managing vehicle access. Below are the different scenarios the system handles:

- **Visitor:**
  <div style="text-align: center;">
    <img src="https://github.com/user-attachments/assets/1c4257dc-d358-417c-87d5-e3f0d4c08871" alt="Visitor Access" width="300">
  </div>
  - The system detects a visitor’s vehicle, extracts the license plate number, and verifies it against the visitor records. The user is identified as a visitor, and access is granted accordingly.

- **Resident:**
  <div style="text-align: center;">
    <img src="https://github.com/user-attachments/assets/69388b48-3771-476a-8936-ee325230a97d" alt="Resident Access" width="300">
  </div>
  - When a resident’s vehicle approaches the gate, the system quickly recognizes the license plate, identifies the user as a resident, and access is granted accordingly.

- **Unknown:**
  <div style="text-align: center;">
    <img src="https://github.com/user-attachments/assets/9cf6502f-763d-42eb-b8b6-7861a6d3e777" alt="Unknown Access" width="300">
  </div>
  - If an unregistered vehicle is detected, the system flags it as "None," displays the license plate number with a "None" role, and keeps the gate closed for security purposes.

### Web Interface

The AutoGate AI web interface allows administrators and residents to manage access records and review historical data easily. Here’s a video demonstration of the interface in action:

[Web Interface Demo.webm](https://github.com/user-attachments/assets/65b62abc-88f7-4329-a0bd-48053f86c5f0)

The video showcases how to navigate the dashboard, manage visitor and resident records, and view historical access logs, all through a clean and user-friendly interface.

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.