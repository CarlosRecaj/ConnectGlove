# 🧤 ConnectGlove

*An intelligent wearable and edge-AI solution for translating one-handed Spanish Sign Language (LSE) into text in real-time. Built for Hackestiu 2026.*

<p align="center">
  <br><br>
  <img src="assets\img\Program execution.jpeg" alt="ConnectGlove Main Photo" width="700"/>
  <br><br>
</p>

---

## 👥 The Team & Affiliations

This project was developed during Hackestiu 2026 by:

| Name | Affiliation | GitHub |
| :--- | :--- | :--- |
| **Pau Pujol Romeu** | UPC - ETSETB | [@paupujol9376](https://github.com/paupujol9376) |
| **Sonia Galduf Gosálvez** | UPC - ETSETB | [@soniagg0](https://github.com/soniagg0) |
| **Ignasi Albert Hohenhorst** | UPC - FIB | [@ignasial](https://github.com/ignasial) |
| **Carlos Recaj Peraire** | UPC - ETSETB | [@CarlosRecaj](https://github.com/CarlosRecaj) |



---

## 📖 About The Project. 

### Motivation. 
Millions of non-verbal people rely on sign language for everyday communication. However, communication barriers still exist because most people do not understand sign language. Our project aims to help bridge this gap by training a computer vision model capable of translating sign language into text in real time while running entirely on an Edge device.

### Solution. 
**ConnectGlove** captures hand movements and positions via an HD camera and a custom glove prototype that increases model precision. It interprets them through an Artificial Intelligence model trained specifically for the LSE fingerspelling alphabet and one-handed gestures.

> **Acknowledgments:** This project is heavily inspired by and based on the [Edge Impulse Rock-Paper-Scissors Arduino UNO Q Example](https://github.com/edgeimpulse/example-rock-paper-scissors-Arduino-UNO-Q/blob/main/README.md). We adapted their excellent computer vision deployment pipeline to fit our sign-language recognition needs.

### 🎥 Project Video & Documentation

<p align="center">
  <br><br>
  <!-- 📷 [PLACEHOLDER: Add a link/thumbnail to your English demonstration video] -->
  <a href="YOUR_VIDEO_URL">
    <img src="https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg" alt="Watch the demonstration video" width="600"/>
  </a>
  <br><br>
</p>

### ✨ Key Features
*   **Real-time detection:** Gesture recognition with no perceivable delay.
*   **One-handed focus:** Optimized for signs that can be performed with a single hand.
*   **Edge Computing:** Runs completely locally on an Edge device (Arduino Uno Q) without requiring internet access.
*  **Privacity:** The local model ensures users privacity. 
*   **Open Source:** Open and accessible code so it can be replicated by anyone.

---

## 🛠️ Built With

*   **Languages:** Arduino App Lab, Python
*   **Machine Learning:** EdgeImpulse using a pre-trained model (`MobileNetV2 SSD FPN-Lite`)
*   **Hardware:** Arduino Uno Q + USB-C Hub + USB-C HD Camera
*   **Glove:** Custom Glove Prototype

<p align="center">
  <br><br>
  <img src="assets\img\glove.jpg" alt="Glove Prototype" width="600"/>
  <br><br>
</p>

---

## 🧠 Model & Data

The gesture recognition model was trained using **Edge Impulse**. You can view, clone, and test the public model directly here: 
👉 **[Link to our Public Edge Impulse Project / Model](https://studio.edgeimpulse.com/studio/1070149)**

### Dataset & Training
<p align="center">
  <br>
  <img src="assets\img\data_adq.png" alt="Dataset and Bounding Boxes" width="600"/>
  <br>
  <em>Dataset collection and labeling process for the LSE gestures.</em>
  <br><br>
</p>

### Results & Metrics
<p align="center">
  <br>
  <img src="assets\img\metrics.jpg" alt="Training Metrics and Confusion Matrix" width="600"/>
  <br>
  <em>Model training performance and confusion matrix results.</em>
  <br><br>
</p>
<p align="center">
  <br>
  <img src="assets\img\detection.jpg" alt="Training Metrics and Confusion Matrix" width="600"/>
  <br>
  <em>Model detection.</em>
  <br><br>
</p>


---

## 🚀 How to Reproduce the Project

### Prerequisites
* Arduino UNO Q with Arduino App Lab.
* USB camera connected to the board.
* Edge Impulse machine learning model trained to detect signs (you can clone an existing public project and re-train it to improve the accuracy with your light and background).

### Step 1: Transfer the app
1. Clone this repository to your local machine.
2. Copy the entire project folder to the Arduino UNO Q board via SSH: `scp -r ConnectGlove/ arduino@<device-ip>:/home/arduino/ArduinoApps/ConnectGlove`.
3. Alternatively, use the Arduino App Lab **Create new App** button in the *My Apps* section and import the application. 

### Step 2: Deploy the model
1. Get into the ConnectGlove app inside the Arduino App Lab.
2. Click in the **Brick Video Object Detection** and then click **Train new AI model** in the bottom.
3. Log in into your Arduino account and the Edge Impulse account to train your own model.
4. Deploy the model as **Arduino UNO Q** or as **Linux aarch64**.
5. The deployed models will appear in the brick of the Arduino App Lab when you go to the *AI models* tab. Select your custom model.
6. Check that it is being added in the `app.yaml` file of the app.

<p align="center">
  <br>
  <!-- 📷 [PLACEHOLDER: Add a screenshot of the Arduino App Lab / Model selection here] -->
  <img src="URL_TO_APP_LAB_SCREENSHOT.jpg" alt="Arduino App Lab Deployment" width="600"/>
  <br><br>
</p>

### Step 3: Start the app
1. Launch the Arduino App Lab in your local machine and get into your Arduino UNO Q .
2. Go to *My Apps*, click on the ConnectGlove application, and then click **Run** .
3. Alternatively, via SSH you can start the application using the CLI: `arduino-app-cli app start user:connectglove`.
4. Once successfully started, navigate to `http://<device-ip>:5001` in your browser and start translating signs!

<p align="center">
  <br>
  <!-- 📷 [PLACEHOLDER: Add a screenshot of the web interface running at port 5001 here] -->
  <img src="URL_TO_WEB_INTERFACE.jpg" alt="Web Interface" width="600"/>
  <br><br>
</p>

### Configuration
All settings are in `python/main.py` at the top:

| Setting | Default | Description |
| :--- | :--- | :--- |
| `CONFIDENCE_THRESHOLD` | 0.6 | Minimum confidence to accept a detection   |
| `PORT` | 5001 | Flask web server port (also set FLASK_PORT env var)  |

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
