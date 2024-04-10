import importlib
import math
import threading
import time

import cv2

# Global variables
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 960
CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_FPS = 1280, 960, 30
DNX64_PATH = "C:\\Program Files\\DNX64\\DNX64.dll"
DEVICE_INDEX = 0
# Camera index, please change it if you have more than one camera,
# i.e. webcam, connected to your PC until CAM_INDEX is been set to first Dino-Lite product.
CAM_INDEX = 0
# Buffer time for Dino-Lite to return value
QUERY_TIME = 0.05
# Buffer time to allow Dino-Lite to process command
COMMAND_TIME = 0.25


def clear_line(n=1):
    LINE_CLEAR = "\x1b[2K"
    for i in range(n):
        print("", end=LINE_CLEAR)


def threaded(func):
    """Wrapper to run a function in a separate thread with @threaded decorator"""

    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()

    return wrapper


def custom_microtouch_function():
    """Executes when MicroTouch press event got detected"""

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    clear_line(1)
    print(f"{timestamp} MicroTouch press detected!", end="\r")


def print_amr(microscope):
    config = microscope.GetConfig(DEVICE_INDEX)
    if (config & 0x40) == 0x40:
        amr = microscope.GetAMR(DEVICE_INDEX)
        amr = round(amr, 1)
        clear_line(1)
        print(f"{amr}x", end="\r")
        time.sleep(QUERY_TIME)
    else:
        clear_line(1)
        print("It does not belong to the AMR serie.", end="\r")


def print_config(microscope):
    config = microscope.GetConfig(DEVICE_INDEX)
    clear_line(1)
    print("Config value =", end="")
    print("0x{:X}".format(config), end="")
    if (config & 0x80) == 0x80:
        print(", EDOF", end="")
    if (config & 0x40) == 0x40:
        print(", AMR", end="")
    if (config & 0x20) == 0x20:
        print(", eFLC", end="")
    if (config & 0x10) == 0x10:
        print(", Aim Point Laser", end="")
    if (config & 0xC) == 0x4:
        print(", 2 segments LED", end="")
    if (config & 0xC) == 0x8:
        print(", 3 segments LED", end="")
    if (config & 0x2) == 0x2:
        print(", FLC", end="")
    if (config & 0x1) == 0x1:
        print(", AXI")
    print("", end="\r")
    time.sleep(QUERY_TIME)


def set_index(microscope):
    microscope.SetVideoDeviceIndex(0)
    time.sleep(COMMAND_TIME)


def print_fov_mm(microscope):
    amr = microscope.GetAMR(DEVICE_INDEX)
    fov = microscope.FOVx(DEVICE_INDEX, amr)
    amr = round(amr, 1)
    fov = round(fov / 1000, 2)
    if fov == math.inf:
        fov = round(microscope.FOVx(DEVICE_INDEX, 50.0) / 1000.0, 2)
        clear_line(1)
        print("50x fov: ", fov, "mm", end="\r")
    else:
        clear_line(1)
        print(f"{amr}x fov: ", fov, "mm", end="\r")
    time.sleep(QUERY_TIME)


def print_deviceid(microscope):
    clear_line(1)
    print(microscope.GetDeviceId(0), end="\r")
    time.sleep(QUERY_TIME)


@threaded
def flash_leds(microscope):
    microscope.SetLEDState(0, 0)
    time.sleep(COMMAND_TIME)
    microscope.SetLEDState(0, 1)
    time.sleep(COMMAND_TIME)
    clear_line(1)
    print("flash_leds", end="\r")


def led_off(microscope):
    microscope.SetLEDState(0, 0)
    time.sleep(COMMAND_TIME)
    clear_line(1)
    print("led off", end="\r")


def capture_image(frame):
    """Capture an image and save it in the current working directory."""

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"image_{timestamp}.png"
    cv2.imwrite(filename, frame)
    clear_line(1)
    print(f"Saved image to {filename}", end="\r")


def start_recording(frame_width, frame_height, fps):
    """Start recording video and return the video writer object."""

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"video_{timestamp}.avi"
    fourcc = cv2.VideoWriter.fourcc(*"XVID")
    video_writer = cv2.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))
    clear_line(1)
    print(f"Video recording started: {filename}. Press r to stop.", end="\r")
    return video_writer


def stop_recording(video_writer):
    """Stop recording video and release the video writer object."""

    video_writer.release()
    clear_line(1)
    print("Video recording stopped", end="\r")


def initialize_camera():
    """
    Setup OpenCV camera parameters and return the camera object.
    Change CAM_INDEX to Dino-Lite camera index, which is based on the order of the camera connected to your PC.
    Read the full doc of `cv2.VideoCapture()` at
    https://docs.opencv.org/4.5.2/d8/dfe/classcv_1_1VideoCapture.html#aabce0d83aa0da9af802455e8cf5fd181 &
    https://docs.opencv.org/3.4/dd/d43/tutorial_py_video_display.html
    """

    camera = cv2.VideoCapture(CAM_INDEX, cv2.CAP_DSHOW)
    camera.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc("m", "j", "p", "g"))
    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc("M", "J", "P", "G"))
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    return camera


def process_frame(frame):
    """Resize frame to fit window."""

    return cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))


def init_microscope(microscope):
    # Set index of video device. Call before Init().
    microscope.SetVideoDeviceIndex(DEVICE_INDEX)
    time.sleep(0.1)
    # Enabled MicroTouch Event
    microscope.EnableMicroTouch(True)
    time.sleep(0.1)
    # Function to execute when MicroTouch event detected
    microscope.SetEventCallback(custom_microtouch_function)
    time.sleep(0.1)

    return microscope


def print_keymaps():
    print(
        "Press the key below prompts to continue \n \
        0:Led off \n \
        1:AMR \n \
        2:Flash_leds and On \n \
        c:List config \n \
        d:Show devicd id \n \
        f:Show fov \n \
        r:Record video or Stop Record video \n \
        s:Capture image \n \
        6:Set EFLC Quddrant 1 to flash \n \
        7:Set EFLC Quddrant 2 to flash \n \
        8:Set EFLC Quddrant 3 to flash \n \
        9:Set EFLC Quddrant 4 to flash \n \
        Esc:Quit \
        "
    )


def config_keymaps(microscope, frame):
    key = cv2.waitKey(1) & 0xFF

    # Press '0' to set_index()
    if key == ord("0"):
        led_off(microscope)

    # Press '1' to print AMR
    if key == ord("1"):
        print_amr(microscope)

    # Press '2' to flash LEDs
    if key == ord("2"):
        flash_leds(microscope)

    # Press 'c' to save a snapshot
    if key == ord("c"):
        print_config(microscope)

    # Press 'd' to show device id
    if key == ord("d"):
        print_deviceid(microscope)

    # Press 'f' to show fov
    if key == ord("f"):
        print_fov_mm(microscope)

    # Press 's' to save a snapshot
    if key == ord("s"):
        capture_image(frame)

    # Press '6' to let EFCL Quadrant 1 to flash
    if key == ord("6"):
        microscope.SetEFLC(DEVICE_INDEX, 1, 32)
        time.sleep(0.1)
        microscope.SetEFLC(DEVICE_INDEX, 1, 31)

    # Press '7' to let EFCL Quadrant 2 to flash
    if key == ord("7"):
        microscope.SetEFLC(DEVICE_INDEX, 2, 32)
        time.sleep(0.1)
        microscope.SetEFLC(DEVICE_INDEX, 2, 15)

    # Press '8' to let EFCL Quadrant 3 to flash
    if key == ord("8"):
        microscope.SetEFLC(DEVICE_INDEX, 3, 32)
        time.sleep(0.1)
        microscope.SetEFLC(DEVICE_INDEX, 3, 15)

    # Press '9' to let EFCL Quadrant 4 to flash
    if key == ord("9"):
        microscope.SetEFLC(DEVICE_INDEX, 4, 32)
        time.sleep(0.1)
        microscope.SetEFLC(DEVICE_INDEX, 4, 31)

    return key


def start_camera(microscope):
    """Starts camera, initializes variables for video preview, and listens for shortcut keys."""

    camera = initialize_camera()

    if not camera.isOpened():
        print("Error opening the camera device.")
        return

    recording = False
    video_writer = None
    inits = True

    print_keymaps()

    while True:
        ret, frame = camera.read()
        if ret:
            resized_frame = process_frame(frame)
            cv2.imshow("Dino-Lite Camera", resized_frame)

            if recording:
                video_writer.write(frame)
            # Only initialize once in this while loop
            if inits:
                microscope = init_microscope(microscope)
                inits = False

        key = config_keymaps(microscope, frame)

        # Press 'r' to start recording
        if key == ord("r") and not recording:
            recording = True
            video_writer = start_recording(CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_FPS)

        # Press 'r' again to stop recording
        elif key == ord("r") and recording:
            recording = False
            stop_recording(video_writer)

        # Press ESC to close
        if key == 27:
            clear_line(1)
            break

    if video_writer is not None:
        video_writer.release()
    camera.release()
    cv2.destroyAllWindows()


def run_usb():
    try:
        DNX64 = getattr(importlib.import_module("DNX64"), "DNX64")
    except ImportError as err:
        print("Error: ", err)

    # Initialize microscope
    micro_scope = DNX64(DNX64_PATH)
    start_camera(micro_scope)


# if __name__ == "__main__":
