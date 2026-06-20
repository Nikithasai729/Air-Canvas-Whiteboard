# download_model.py
import urllib.request

url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"
output = "hand_landmarker.task"

print("Downloading hand tracking asset file... Please hold on.")
urllib.request.urlretrieve(url, output)
print("Success! 'hand_landmarker.task' downloaded successfully to your folder.")