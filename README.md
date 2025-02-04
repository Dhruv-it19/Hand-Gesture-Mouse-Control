# 🖱️ Hand Gesture Mouse Control using OpenCV & MediaPipe

This project enables **mouse control using hand gestures** via a webcam. It uses **MediaPipe** for hand tracking and **AutoPy** for controlling the mouse cursor.

## 📌 Features
✅ **Move the cursor** using your index finger  
✅ **Click with your thumb & index finger**  
✅ **Smooth mouse movements** using interpolation  
✅ **No hand skeleton (finger connections) drawn**  

## 📂 Installation

### **1️⃣ Install Dependencies**

Before running the code, install the required Python libraries:

pip install opencv-python numpy mediapipe autopy

### **2️⃣ Clone this repository**

git clone https://github.com/Dhruv-it19/Hand-Gesture-Mouse-Control.git

cd hand-gesture-mouse

### **3️⃣ Run the script**

python `hand_mouse.py`


## **🎮 Usage Instructions**

Ensure your webcam is connected and running.

Raise your index finger to move the cursor.

Pinch (touch index finger & thumb) to click.

Press the spacebar (␣) to exit.

## **🛠️ Troubleshooting**

❌ Cursor movement is not accurate?

✔ Adjust the `smoothening` variable in the code.

❌ Webcam not detected?

✔ Change `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)`.

❌ ModuleNotFoundError: No module named 'autopy'

✔ Run `pip install autopy` (some systems may require pip install autopy --user).

## **💡 Future Improvements**

🔹 Add drag & drop functionality

🔹 Support multiple gestures for more actions
