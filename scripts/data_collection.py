import sys
import os
import cv2


# # Thêm thư mục config vào sys.path
sys.path.append(os.path.join(os.getcwd(), 'config'))
from config.setting import DATA_DIR, HAARCASCADE_DIR, IMG_SIZE, MAX_IMAGES_PER_STUDENT

# python -m scripts.data_collection

def collect_faces():
    """Collect face images from the webcam."""
    student_name = input("Enter student name: ")
    student_id = input("Enter student ID: ")
    save_dir = os.path.join(DATA_DIR, f"{student_id}_{student_name}")
    frontalface_dir = os.path.join(HAARCASCADE_DIR, "haarcascade_frontalface_default.xml")
    os.makedirs(save_dir, exist_ok=True)

    face_cascade = cv2.CascadeClassifier(frontalface_dir)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Unable to open webcam. Please check the connection!")
        return

    cap.set(3, 720)  # Width resolution
    cap.set(4, 576)  # Height resolution

    count = 0
    collecting = False

    print("🔹 Press 'S' to start collecting images, 'Q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Unable to capture image from webcam.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if collecting and count < MAX_IMAGES_PER_STUDENT:
                face_img = frame[y:y+h, x:x+w]
                face_img = cv2.resize(face_img, IMG_SIZE)  # Resize image to standard size
                file_name = os.path.join(save_dir, f"{count}.jpg")
                cv2.imwrite(file_name, face_img)
                count += 1

        # Display instructions on the screen
        cv2.putText(frame, f"Images collected: {count}/{MAX_IMAGES_PER_STUDENT}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'S' to start collecting", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'Q' to exit", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Face Collection", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            collecting = True
            print("🟢 Image collection started...")
        elif key == ord('q') or count >= MAX_IMAGES_PER_STUDENT:
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"✅ Collected {count} images for {student_name} ({student_id})")

if __name__ == "__main__":
    collect_faces()
