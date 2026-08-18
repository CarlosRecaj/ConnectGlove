# ConnectGlove
Repository for ConnectGlove (Hackestiu 2026). The project focuses on detecting one-handed Spanish Sign Language

## Motivation

Millions of non-verbal people rely on sign language for everyday communication. However, communication barriers still exist because most people do not understand sign language. Our project aims to help bridge this gap by training a computer vision model capable of translating sign language into text in real time while running on an Edge device as Arduino Uno Q. 

## The Project

ConnectGlove captures hand movements and positions, interpreting them through an Artificial Intelligence model trained specifically for the LSE fingerspelling alphabet and one-handed gestures using our glove prototype that increases the model precision.

### Key Features:

Real-time detection: Gesture recognition with no perceivable delay.

One-handed focus: Optimized for signs that can be performed with a single hand.

Open Source: Open and accessible code so it can be replicated by anyone.

Running on an edge device

## Built With

Languages: Python, Arduino 

Machine Learning: EdgeImpulse using pre-trained model MobileNetV2 SSD FPN-Lite

Hardware: Arduino Uno Q + USB-C Hub + USB-C HD camera

<!--
## Methodology

Hardware setup / Data capture: We configured the data capture system [explain if it's a physical glove with sensors or a webcam-based system using MediaPipe].

Processing and Training (Machine Learning): We processed the data to extract hand coordinates and features, training a classification model [e.g., Neural Network, Random Forest] to predict signs with high accuracy.

Integration and Interface: The prediction model was connected to a [web / desktop] application that instantly displays the inferred letter or word, with the option to [play it as audio text-to-speech].

⚙️ Getting Started

To get a local copy up and running, follow these simple steps.

Prerequisites

Python 3.8 or higher

[Other requirements, e.g., a webcam]

Installation

Clone the repository:

git clone https://github.com/your-username/ConnectGlove.git
cd ConnectGlove


Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate


Install the dependencies:

pip install -r requirements.txt


Usage

To start the detector, run the following command:

python main.py


(Explain briefly here how to use the app, e.g., "Press 'Q' to quit", "Hold your hand in front of the camera", etc.)

🔮 Future Work (Roadmap)

Despite the success achieved during Hackestiu 2026, we have many ideas to continue improving the project:

[ ] Expand the dataset to include facial expressions.

[ ] Train the model to predict full sentences or dynamic signs, not just static ones.

[ ] Develop a mobile application for iOS and Android.

[ ] Design a custom PCB for the glove [if it's a hardware-based project].

🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

👥 The Team

[Your Name or Member 1] - [Role, e.g., ML Developer] - [GitHub/LinkedIn link]

[Member 2 Name] - [Role, e.g., Hardware / Frontend] - [GitHub/LinkedIn link]

[Member 3 Name] - [Role, e.g., UI/UX Designer] - [GitHub/LinkedIn link]

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.-->
