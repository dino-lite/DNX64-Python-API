# Appendix: Parameter Table

Below parameter tables explain further details of corresponding `DNX64` API.

### GetConfig():

| Bit   | Name | Type | Value                            |
| ----- | ---- | ---- | -------------------------------- |
| [7]   | EDOF | Read | 1 = Supported, 0 = Not supported |
| [6]   | AMR  | Read | 1 = Supported, 0 = Not supported |
| [5]   | eFLC | Read | 1 = Supported, 0 = Not supported |
| [4]   | APL  | Read | 1 = Supported, 0 = Not supported |
| [3:2] | LED  | Read | 00 = Not switchable              |
|       |      |      | 01 = 2 Modes (on & off)          |
|       |      |      | 10 = 3 Modes (LED 1, LED2, off)  |
|       |      |      | 11 = Reserved                    |
| [1]   | FLC  | Read | 1 = Supported, 0 = Not supported |
| [0]   | AXI  | Read | 1 = Supported, 0 = Not supported |

### Video Index of [Get/Set]VideoProcAmp()

| Value | Parameter             |
| ----- | --------------------- |
| 0     | Brightness            |
| 1     | Contrast              |
| 2     | Hue                   |
| 3     | Saturation            |
| 4     | Sharpness             |
| 5     | Gamma                 |
| 6     | ColorEnable           |
| 7     | WhiteBalance          |
| 8     | BacklightCompensation |
| 9     | Gain                  |

### SetExposure()

| Series       | Exposure Range |
| ------------ | -------------- |
| 3011, 3013   | 8 to 30612     |
| 1.3M Edge    | 1 to 63076     |
| 5M Edge      | 1 to 30000     |
| 1.3M Premier | 1 to 41771     |
| 5M Premier   | 1 to 30000     |

### SetFLCSwitch()

| Value | Switch-on Quadrant |
| ----- | ------------------ |
| 1     | 1                  |
| 2     | 2                  |
| 3     | 1, 2               |
| 4     | 3                  |
| 5     | 1, 3               |
| 6     | 2, 3               |
| 7     | 1, 2, 3            |
| 8     | 4                  |
| 9     | 1, 4               |
| 10    | 2, 4               |
| 11    | 1, 2, 4            |
| 12    | 3, 4               |
| 13    | 1, 3, 4            |
| 14    | 2, 3, 4            |
| 15    | 1, 2, 3, 4         |
| 16    | All LEDs turn off  |

### SetLEDState()

- LED2 only exists on models with 2 switchable LEDs.

| Values | Description |
| ------ | ----------- |
| 0      | LED off     |
| 1      | LED1 on     |
| 2      | LED2 on.    |
