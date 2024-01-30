if __name__ == "__main__":
    import cv2

    # Camera index, please change it if you have more than one camera,
    # i.e. webcam, connected to your PC until CAM_INDEX is been set to first Dino-Lite product.
    CAM_INDEX = 0

    # Change CAM_INDEX to Dino-Lite camera index, which is based on the order of the camera connected to your PC.
    # Read the full doc of `cv2.VideoCapture()` at
    # https://docs.opencv.org/4.5.2/d8/dfe/classcv_1_1VideoCapture.html#aabce0d83aa0da9af802455e8cf5fd181 &
    # https://docs.opencv.org/3.4/dd/d43/tutorial_py_video_display.html

    cap = cv2.VideoCapture(CAM_INDEX)

    # Press ESC to exit preview window
    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imshow("frame", frame)
        key = cv2.waitKey(1)
        # ESC
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
