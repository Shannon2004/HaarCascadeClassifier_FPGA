import cv2
import numpy as np
import xml.etree.ElementTree as ET
import time


def integral_img_cal(img_arr):
    integral_img = np.zeros((img_arr.shape[0],img_arr.shape[1]))
    integral_img = np.cumsum(np.cumsum(img_arr, axis=0), axis=1)
    return integral_img


# Function to parse XML and extract stage thresholds, weak classifiers, and features
def parse_haar_cascade_xml(xml_file):
    # Load the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    stages_info = []  # Store all relevant info for each stage: weak classifiers and stage thresholds
    features = []  # Store Haar features (rectangles)
    
    # Locate the 'stages' element inside the 'cascade' tag
    stages = root.find('cascade').find('stages')
    
    # Iterate through stages
    for stage in stages:
        # Extract the stage threshold
        stage_threshold = float(stage.find('stageThreshold').text.strip())
        stage_weak_classifiers = []  # Temporary storage for weak classifiers in the stage
        
        # Extract weak classifiers within each stage
        weak_classifiers = stage.find('weakClassifiers')
        for classifier in weak_classifiers:
            internal_node = classifier.find('internalNodes').text.strip().split()
            leaf_values = classifier.find('leafValues').text.strip().split()
            
            # Parse internal nodes and leaf values
            internal_node = list(map(float, internal_node))
            leaf_values = list(map(float, leaf_values))

            stage_weak_classifiers.append({
                'internalNodes': internal_node,
                'leafValues': leaf_values
            })
        
        # Store all relevant stage info (weak classifiers + stage threshold)
        stages_info.append({
            'stageThreshold': stage_threshold,
            'weakClassifiers': stage_weak_classifiers
        })

    # Extract features (rectangles) from the XML
    feature_params = root.find('cascade').find('features')
    if feature_params is not None:
        for feature in feature_params:
            rects = []
            for rect in feature.find('rects'):
                rect_values = list(map(float, rect.text.strip().split()))
                rects.append(rect_values)
            features.append(rects)
    
    return stages_info, features

# function to calculate the std deviation of the window
def std_deviation(gray_img_arr,su,sd,eu,ed):
      mask = np.zeros(gray_img_arr.shape, dtype=np.uint8)
      pts = np.array([su, sd, ed, eu], dtype=np.int32)
      cv2.fillPoly(mask, [pts], 255)
      masked_image = cv2.bitwise_and(gray_img_arr, gray_img_arr, mask=mask)
      pixels_in_window = masked_image[mask == 255]
      return np.std(pixels_in_window)

def decision_weak_classifier(img_size, wsize, feature, wclassifier, integral_img, su, std_dev_value):
    feature_value = 0
    weighted_intensity_sum = 0
    
    # Loop over all rectangles in the feature (there can be at max 3)
    for rect in feature:
        tl = np.array([int(su[0] + rect[1]), int(su[1] + rect[0])])
        bl = np.array([int(tl[0] + rect[3]-1), int(tl[1])])
        tr = np.array([int(tl[0]), int(tl[1] + rect[2]-1)])
        br = np.array([int(tl[0] + rect[3]-1), int(tl[1] + rect[2]-1)])

        if (br[0] >= img_size[0] or br[1] >= img_size[1] or
            bl[0] >= img_size[0] or bl[1] < 0 or
            tr[0] < 0 or tr[1] >= img_size[1]):
            continue  

        intensity_sum = (
            integral_img[br[0]][br[1]] 
            + integral_img[tl[0]][ tl[1]] 
            - integral_img[bl[0]][ bl[1]] 
            - integral_img[tr[0]][ tr[1]]
        )
        
        weighted_intensity_sum += intensity_sum * rect[-1]
    weighted_intensity_sum = np.mean(weighted_intensity_sum)
    print('Weighted Intensity Sum:', weighted_intensity_sum, 
          'Classifier Threshold:', wclassifier['internalNodes'][-1])
        
    # Compare the weighted intensity sum to the classifier threshold
    if weighted_intensity_sum > wclassifier['internalNodes'][-1]:
        feature_value = wclassifier['leafValues'][0]
        print("Going left to node with value:", feature_value)
        print()
    else:
        feature_value = wclassifier['leafValues'][1]
        print("Going right to node with value:", feature_value)
        print()

    return feature_value

def stage_calculation_decision(img_size, wsize, features, integral_img, su, stageinfo, std_dev_value):
    stage_value = 0
    stage_threshold = stageinfo['stageThreshold']
    global STAGE_NUMBER
    STAGE_NUMBER += 1
    print(" NEW STAGE :",STAGE_NUMBER, "")
    print(f"Processing stage with threshold: {stage_threshold}")
    
    for i in range(len(stageinfo['weakClassifiers'])):
        feature_index = int(stageinfo['weakClassifiers'][i]['internalNodes'][2])
        feature = features[feature_index]
        wclassifier = stageinfo['weakClassifiers'][i]
        feature_value = decision_weak_classifier(img_size, wsize, feature, wclassifier, integral_img, su, std_dev_value)
        stage_value += feature_value
        
        # print(f"Iteration {i + 1}: feature value = {feature_value}, cumulative stage value = {stage_value}")

    print(f"Stage number: {STAGE_NUMBER} Final stage value: {stage_value}, Stage threshold: {stage_threshold}")
    if (stage_value > stage_threshold):
        return 1
    else:
        return 0





# Original Image Read
original_img = cv2.imread('preprocessed_image_plt.png')

# Calculate mean and standard deviation for RGB channels
mean, std = cv2.meanStdDev(original_img)
print('Mean:', mean)
print('Standard Deviation:', std)

# Standardize the original image using the mean and std
mean = mean.reshape(1, 1, 3)  # Reshape to (1, 1, 3)
std = std.reshape(1, 1, 3)      # Reshape to (1, 1, 3)
# Standardize the image: (image - mean) / std
img = (original_img - mean) / std
img_arr = np.array(img)

print("Standardized Image")
print(img_arr)

# Calculate integral image from the RGB image
integral_img = integral_img_cal(img_arr)  # Use standardized RGB image
print("Integral Image")
print(integral_img)

# Remove the grayscale conversion
# Use the original image in the decision-making part instead of the grayscale image.
img_size = original_img.shape[:2]  # Height, Width of the original image
wsize = 24
STAGE_NUMBER = 0


# IMPLEMENTING FEATURE 1 WHILE MOVING A 24X24 WINDOW ACROSS THE WHOLE IMAGE
# FEATURE 1 WILL CORRESPOND TO ONE WEAK CLASSIFIER
# EACH WEAK CLASSIFIER HAS FOUR VALUES:
# 1) INDEX OF LEFT NODE OF CLASSIFIER
# 2) INDEX OF RIGHT NODE OF CLASSIFIER
# 3) WHICH FEATURE THE WEAK CLASSFIER CORRESPONDS TO
# 4) THE THRESHOLD VALUE OF THE WEAK CLASSIFIER. IF THE FEATURE VALUE IS GREATER THAN THE THRESHOLD WILL GO TO THE LEFT NODE (0) OR ELSE IT WILL GO TO THE RIGHT (1)

# INFO ABOUT EACH FEATURE
# EACH FEATURE IS DEFINED AS
#  <rects>
#         <_>
#           6 4 12 9 -1.</_>
#         <_>
#           6 7 12 3 3.</></rects></>
# EACH FEATURE HAS TWO RECTANGLES. ONE IS FOR THE BRIGHT SIDE (POSITIVE WEIGHT)OF THE HAAR FEATURE AND THE OTHER IS DARK REGION OF HAAR FEATURE (NEGATIVE WEIGHT).
# EACH RECTANGLE HAS 5 VALUES.
# 1) THE FIRST TWO VALUES ARE X AND Y COORDINATES OF TOP LEFT CORNER RELATIVE TO THE 24X24 SUB WINDOW.
# 2) THE THIRD AND FOURTH VALUES ARE WIDTH AND HEIGHT OF THE RECTANGLE FROM TOP LEFT CORNER
# 3) THE FIFTH VALUE IS THE WEIGHT OF THE RECTANGLE









# Example usage
xml_file = 'haarcascade_frontalface_default.xml'
stages_info, features = parse_haar_cascade_xml(xml_file)

# Output result for debugging
print("Number of stages:", len(stages_info))





# Declaring the intial window indices
su = np.array([0,0])  # su = top left index
eu = np.array([0,wsize-1])  # eu = top right index
sd = np.array([wsize-1,0])  # sd = bottom -left index of rect
ed = np.array([wsize-1,wsize-1]) # ed = bottom-right index of rect 

# print(img_size[0]-1)

no_stages = len(stages_info)
print(no_stages)
face_bounding_boxes = []

count1 = 0

print(img_size)


# In your main loop
while((ed[0] <= img_size[0]-1) and (ed[1] <= img_size[1]-1)):
    count = 0
    face_region = [su, eu, sd, ed]

    for i in range(no_stages):
        stage_decision = stage_calculation_decision(img_size, wsize, features, integral_img, su, stages_info[i], 1)
        if(stage_decision == 0):
            print(f"Stage {i + 1} failed, stopping early.")
            break
        count += 1
    
    if (count == no_stages):
        face_bounding_boxes.append(face_region)
        print("Face detected! Current bounding box:", face_region)

    # Move the window as before
    if ((eu[1] >= img_size[1]-1) or (ed[1] >= img_size[1]-1) or (su[1] >= img_size[1]-wsize) or (sd[1] >= img_size[1]-wsize)):
        su[0] += 1
        su[1] = 0
        eu[0] += 1
        eu[1] = wsize - 1
        sd[0] += 1
        sd[1] = 0
        ed[0] += 1
        ed[1] = wsize - 1
    else:
        su[1] += 1
        eu[1] += 1
        sd[1] += 1
        ed[1] += 1

print("Total face bounding boxes detected:", len(face_bounding_boxes))
# apply and show
# Convert original image to RGB format if it is in BGR format (common in OpenCV)
original_img_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
# Draw bounding boxes on the original image using matplotlib
def draw_bounding_boxes_with_plt(image, boxes):
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    fig, ax = plt.subplots(1)
    ax.imshow(image)

    for box in boxes:
        # Create a rectangle patch
        rect = patches.Rectangle(box[0], 
                                 box[1][1] - box[0][1], 
                                 box[2][0] - box[0][0],
                                 linewidth=2, edgecolor='green', facecolor='none')
        ax.add_patch(rect)

    plt.axis('off')  # Hide axes
    plt.title('Detected Faces')
    plt.show()  # Display the image with bounding boxes

# Draw bounding boxes on the original image using matplotlib
draw_bounding_boxes_with_plt(original_img_rgb, face_bounding_boxes)




