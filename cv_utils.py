import cv2 
import numpy as np

def get_contour_box(contour):
    rect = cv2.minAreaRect(contour)
    lx, ly = np.round(rect[1],0).astype(int)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    return box, lx, ly

def get_contour(gray):
    #gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = max(contours, key=cv2.contourArea)
    return contour

def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized

def read_image_opencv(filepath):
    im_np = cv2.imread(filepath, cv2.IMREAD_COLOR)
    im_np = cv2.cvtColor(im_np, cv2.COLOR_BGR2RGB)
    return im_np

def write_image_opencv(filepath, im_rgb, width_resize=None):
    if width_resize is not None:
        im_rgb = resize(im_rgb, 640)
    im_bgr = cv2.cvtColor(im_rgb, cv2.COLOR_RGB2BGR)
    im_bgr = cv2.imwrite(filepath, im_bgr)

def calculate_iou_mask(mask1, mask2):
    """
    Calculate the Intersection over Union (IoU) for two binary masks.

    Parameters:
    mask1 : 2D NumPy array
            Binary mask for the first object.
    mask2 : 2D NumPy array
            Binary mask for the second object.
            (The dimensions should match with mask1)

    Returns:
    iou : float
          The IoU value.
    """

    # Calculate intersection
    intersection = np.logical_and(mask1, mask2)

    # Calculate union
    union = np.logical_or(mask1, mask2)

    # Calculate IoU
    iou = np.sum(intersection) / np.sum(union)

    return iou

def get_orientation(contour):
    moments = cv2.moments(contour)
    # Calculate centroid
    cx = int(moments['m10'] / moments['m00'])
    cy = int(moments['m01'] / moments['m00'])
    # Calculate orientation angle using central moments
    delta_x2 = moments['mu20']
    delta_y2 = moments['mu02']
    delta_xy = moments['mu11']
    angle = 0.5 * np.arctan(2 * delta_xy / (delta_x2 - delta_y2))
    return angle, (cx, cy)

def rotate_contour(contour, angle, center):
    # Create a rotation matrix
    rot_matrix = cv2.getRotationMatrix2D(center, np.degrees(angle), 1)
    # Apply affine transform to the contour points
    rotated_contour = cv2.transform(contour, rot_matrix)
    return rotated_contour

def translate_contour(contour, offset):
    translated_contour = contour + offset
    return translated_contour

def get_affine_transform_matrix(src_pts, dst_pts):
    return cv2.getAffineTransform(src_pts, dst_pts)

def get_align_img1(img1, img2):
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    
    res = True
    # Feature detection using SIFT
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1_gray, None)
    kp2, des2 = sift.detectAndCompute(img2_gray, None)

    # Feature matching using FLANN
    FLANN_INDEX_KDTREE = 1
    index_params = {'algorithm': FLANN_INDEX_KDTREE, 'trees': 5}
    search_params = {'checks': 50}

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Apply ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # Get coordinates of the good matches
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # Estimate the Affine Transform
    if len(good_matches) > 3:  # At least 3 points are needed to estimate an affine transformation
        affine_transform, inliers = cv2.estimateAffinePartial2D(src_pts, dst_pts, method=cv2.RANSAC, ransacReprojThreshold=3)

        if affine_transform is not None:
            # Warp the image using the Affine Transform
            rows, cols = img2.shape[0], img2.shape[1]
            img1_aligned = cv2.warpAffine(img1, affine_transform[:2], (cols, rows))

            # Save or display the aligned image
            #cv2.imwrite('aligned_image.jpg', img1_aligned)
        else:
            res = False
            print("Failed to compute affine transform.")
    else:
        res = False
        print("Not enough matches for computing the affine transformation.")
    return res, img1_aligned

def get_largest_contour_from_mask(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = max(contours, key=cv2.contourArea)
    return contour


