# DNX64-Python-API

`DNX64/__init__.py` provides a Python API for `DNX64` SDK, which allows users to interact with a Dino-Lite or Dino-Eye device using Python.

Python class: `DNX64` contains class methods corresponding to functions in the SDK, offering functionalities such as setting camera properties, retrieving device information, and controlling cameras.

## Prerequisites

- To utilize DNX64 APIs for Python, ensure that the `DNX64.dll`, `DNX32.dll` and `libusbK.dll` are been placed in the same directory after installing `DNX64`.
  Please contact your [local distributor](https://www.dino-lite.com/contact01.php) to obtain access `DNX64`.

- Verify that you have the latest version of `DNX64.dll`, which is currently `v1.0.11`.
  You may check the DLL's version by running `python3 ./version.py`.
  If you are not using the most recent version of the DLL, kindly contact your [local distributor](https://www.dino-lite.com/contact01.php) to acquire the latest release.

---

## Setup Python Env

```sh
python3 -m venv .venv
pip3 install -r requirements.txt
```

## Usage

Ensure that the device index is set prior to performing any operations, as an incorrect device value may result otherwise.
Utilize the corresponding class methods for interaction with Dino-Lite or Dino-Eye devices.

- Refer to the `DNX64/__init__.py` file for a comprehensive list of available APIs.
- More advanced examples can be found in `examples` directory.
- Make sure you set global variable: `CAM_INDEX` to your first, if there is more than one,
  Dino-Lite product when connected via USB,
  since `OpenCV` will recognize all USB devices with camera, i.e. webcam, etc.
  Read the full doc of `cv2.VideoCapture()` at [ref1](https://docs.opencv.org/4.5.2/d8/dfe/classcv_1_1VideoCapture.html#aabce0d83aa0da9af802455e8cf5fd181)
  & [ref2](https://docs.opencv.org/3.4/dd/d43/tutorial_py_video_display.html)

```py
try:
    DNX64 = getattr(importlib.import_module("DNX64"), "DNX64")
except ImportError as err:
    print("Error: ", err)

# Initialize the DNX64 class
dll_path = "/path/to/DNX64.dll"
micro_scope = DNX64(dll_path)

# Set Device Index first
micro_scope.SetVideoDeviceIndex(0)

# Get total number of video devices being detected
device_count = micro_scope.GetVideoDeviceCount()
print(f"Number of video devices: {device_count}")
# NOTE: Buffer time for devices to set up properly
time.sleep(0.1)

# Set the auto-exposure target value for device 0
micro_scope.SetAETarget(0, 100)
# NOTE: Buffer time for devices to set up properly
time.sleep(0.1)

# Set the exposure value for device 0
micro_scope.SetExposureValue(0, 1000)
```

- Run below command to start a simple preview window when connected via USB.

`python3 ./examples/simple_usb_preview_window.py`

- Open below html file in browser to start a simple preview webpage when connected via internet.

`./examples/simple_wifi_preview_window.html`

---

## Project Wiki

- [Appendix: Parameter Table](https://github.com/dino-lite/DNX64-Python-API/wiki/Appendix:-Parameter-Table).

## Issues

If you encounter problems with current APIs, feel free to file an [issue](https://github.com/dino-lite/DNX64-Python-API/issues)!

## Acknowledgments

We gratefully acknowledge **Dunwell Tech** for providing the foundational code that contributed to the development of the `DNX64 Python API`!
