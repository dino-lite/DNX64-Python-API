# DNX64-Python-API

`DNX64/__init__.py` provides a Python API for `DNX64.dll` SDK, which allows users to interact with a Dino-Lite or Dino-Eye device using Python.

Python class: `DNX64` contains class methods corresponding to functions in the SDK, offering functionalities such as setting camera properties, retrieving device information, and controlling cameras.

## Prerequisites

When using DNX64 API for python, `DNX64.dll` SDK is needed.

Please contact your [local distributor](https://www.dino-lite.com/contact01.php) to obtain access to `DNX64.dll`.

The latest version of `DNX64.dll` is v1.0.8. If you are not using the latest one, contact your local distributor to get the latest release.

---

## Setup Python Env

```sh
python3 -m venv .venv
pip3 install -r requirements.txt
```

## Usage

TODO: It is required to assign the path of `DNX64.dll` to initialize `DNX64` class object. Find and use the corresponding class methods for interacting with Dino-Lite or Dino-Eye devices.

- Read `DNX64/__init__.py` to get the full list of provided APIs.
- Users can check more advanced examples in `examples` directory.

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

# Initialize the control object
if micro_scope.Init():
    # Get total number of video devices being detected
    device_count = micro_scope.GetVideoDeviceCount()
    print(f"Number of video devices: {device_count}")

    # Set the auto-exposure target value for device 0
    micro_scope.SetAETarget(0, 100)

    # Set the exposure value for device 0
    micro_scope.SetExposureValue(0, 1000)
```

---

## Project Wiki

- [Appendix: Parameter Table](https://github.com/dino-lite/DNX64-Python-API/wiki/Appendix:-Parameter-Table).
- [Appendix: Compare to Cpp API](https://github.com/dino-lite/DNX64-Python-API/wiki/Appendix:-Compare-to-Cpp--API)
