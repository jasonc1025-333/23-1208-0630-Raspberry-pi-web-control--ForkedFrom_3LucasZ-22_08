import cv2
from picamera2 import Picamera2

piCam2_Obj = Picamera2()
piCam2_Obj.preview_configuration.main.size=(1920,1080)  # Full Screen: 3280 2464
piCam2_Obj.preview_configuration.main.format = "RGB888"  # 8 bits
piCam2_Obj.start()

while True:
    piCam2_Image_OfPixelsData_Array = piCam2_Obj.capture_array()
    cv2.imshow("preview", piCam2_Image_OfPixelsData_Array)
    if cv2.waitKey(1) == ord('q'):
        break

piCam2_Obj.stop()
cv2.destroyAllWindows()
