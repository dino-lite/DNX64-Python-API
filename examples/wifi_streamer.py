import importlib
import math
import threading
import time

import cv2

# Global variables
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 960
DNX64_PATH = "C:\\Program Files\\DNX64\\DNX64.dll"
DINO_STREAMER = "http://10.10.10.254:8080/?action=stream"
DEVICE_INDEX = 90  # Use 90 for WF-10 / WF-20 Dino-Lite Streamer
# Buffer time for Dino-Lite to return value
QUERY_TIME = 0.05
# Buffer time to allow Dino-Lite to process command
COMMAND_TIME = 0.25


def threaded(func):
    """Wrapper to run a function in a separate thread with @threaded decorator"""

    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

    return wrapper


def custom_microtouch_function():
    """Executes when MicroTouch press detected"""

    print("MicroTouch press detected!")


def get_resolutions(microscope):
    print(microscope.GetWiFiVideoCaps())


def change_resolution(microscope):
    microscope.SetWiFiVideoRes(1280, 1024)


@threaded
def capture_image_wifi(microscope):
    counter = [0]
    counter[0] += 1
    filename = f"streamer_image_{counter[0]}.jpg"
    microscope.GetWiFiImage(filename)
    print(f"Saved image from Wi-Fi Streamer to: {filename}")


def capture_image(frame):
    """Capture an image and save it in the current working directory."""

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"image_{timestamp}.png"
    cv2.imwrite(filename, frame)
    print(f"Saved image to {filename}")


def initialize_camera():
    """Setup OpenCV camera parameters and return the camera object."""

    camera = cv2.VideoCapture(DINO_STREAMER, cv2.CAP_FFMPEG)
    return camera


def process_frame(frame):
    """Resize frame to fit window."""

    return cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))


def start_camera(microscope):
    """Starts camera, initializes variables for video preview, and listens for shortcut keys."""

    camera = initialize_camera()

    if not camera.isOpened():
        print("Error opening the camera device.")
        return

    while True:
        ret, frame = camera.read()
        if ret:
            resized_frame = process_frame(frame)
            cv2.imshow("Dino-Lite Streamer", resized_frame)

        key = cv2.waitKey(25) & 0xFF

        # Press '1' to Change Resolution
        if key == ord("1"):
            change_resolution(microscope)

        # Press '2' to List supported resolution
        if key == ord("2"):
            get_resolutions(microscope)

        # Press 'p' to capture photo from Dino-Lite Streamer
        if key == ord("p"):
            capture_image_wifi(microscope)

        # Press 's' to save a snapshot
        if key == ord("s"):
            capture_image(frame)

        # Press ESC to close
        if key == 27:
            break

    camera.release()
    cv2.destroyAllWindows()


def run_wifi():
    try:
        DNX64 = getattr(importlib.import_module("DNX64"), "DNX64")
    except ImportError as err:
        print("Error: ", err)

    # Initialize microscope
    micro_scope = DNX64(DNX64_PATH)
    micro_scope.SetVideoDeviceIndex(DEVICE_INDEX)
    start_camera(micro_scope)


# if __name__ == "__main__":
