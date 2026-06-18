import cv2
import time
import pyautogui

cap = cv2.VideoCapture("video.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)

frame_num = 0
events = []

boxes = {
    "w": (100, 100, 50, 50),
    "a": (100, 200, 50, 50),
    "s": (200, 200, 50, 50),
    "d": (200, 100, 50, 50),
}

prev_brightness = {k: None for k in boxes}

def get_brightness(frame, x, y, w, h):
    roi = frame[y+10:y+20, x+10:x+20]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    return gray.mean()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    for key, (x, y, w, h) in boxes.items():
        b = get_brightness(frame, x, y, w, h)

        if prev_brightness[key] is not None:
            if prev_brightness[key] - b > 25:  # threshold
                t = frame_num / fps
                events.append((t, key))
                print(f"{t:.3f} -> {key}")

        prev_brightness[key] = b

    frame_num += 1

cap.release()

print("\nPlaying back...")

start = time.perf_counter()

for t, key in events:
    while time.perf_counter() - start < t:
        pass
    pyautogui.press(key)
