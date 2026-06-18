import cv2

# Load video
cap = cv2.VideoCapture("video.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)

frame_num = 0
events = []

# 🔴 YOU WILL CHANGE THESE COORDINATES
boxes = {
    "w": (100, 100, 50, 50),
    "a": (100, 200, 50, 50),
    "s": (200, 200, 50, 50),
    "d": (200, 100, 50, 50),
}

prev_brightness = {k: None for k in boxes}
last_trigger_time = {k: -1 for k in boxes}

cooldown = 0.1  # seconds between triggers

def get_brightness(frame, x, y):
    # sample small center area (reduces noise)
    roi = frame[y+10:y+20, x+10:x+20]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    return gray.mean()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Save first frame to help you find coordinates
    if frame_num == 0:
        cv2.imwrite("first_frame.png", frame)

    for key, (x, y, w, h) in boxes.items():
        b = get_brightness(frame, x, y)

        if prev_brightness[key] is not None:
            change = prev_brightness[key] - b

            if change > 25:
                t = frame_num / fps

                if t - last_trigger_time[key] > cooldown:
                    events.append((round(t, 3), key))
                    print(f"{t:.3f} -> {key}")
                    last_trigger_time[key] = t

        prev_brightness[key] = b

    frame_num += 1

cap.release()

print("\nFinal events:")
print(events)
