import cv2
import numpy as np

# Load the image
# img = cv2.imread("../resources/testing/test-image-1.png")


def convert_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Perform Canny edge detection
    edges = cv2.Canny(blurred, 25, 200)

    # Perform dilation to fill in gaps in the edge map
    kernel = np.ones((5,5), np.uint8)
    # dilated = cv2.dilate(edges, kernel, iterations=1)
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # Find contours in the edge map
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a mask using the contours
    mask = np.zeros_like(closed)
    cv2.drawContours(mask, contours, -1, 255, -1)

    # Extract the object using the mask
    object = cv2.bitwise_and(image, image, mask=mask)

    #return the object
    return object

# object = convert_image(img)
#
# # Save the extracted object as a PNG image
# cv2.imwrite("object.png", object)
#
# # Show the extracted object
# cv2.imshow("Object", object)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
