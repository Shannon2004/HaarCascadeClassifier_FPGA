# FPGA Implementation of Haar Cascade Classifier

## Pre-requisites

### Haar Features
Haar features are rectangular patterns that detect important visual characteristics within a given detection window. These features identify intensity differences between adjacent regions, allowing the classifier to recognize key structural elements such as edges, lines, and textures. Each Haar feature is computed by summing pixel intensities in specific regions and comparing them, making it possible to distinguish significant visual patterns efficiently.

### Integral Image
The integral image is a technique used to accelerate Haar feature computation. It allows for the rapid summation of pixel values within rectangular regions by transforming the original image into a cumulative summed representation. Using this transformation, any rectangular region's sum can be computed in constant time, significantly enhancing the efficiency of Haar feature evaluation.

### Haar Cascade Classifier Architecture
The Haar Cascade classifier operates by scanning a 24×24 detection window across an image and processing it through multiple sequential stages. Each stage consists of a predefined number of Haar features, where each feature corresponds to a weak classifier. These weak classifiers compute feature values and compare them against learned feature thresholds.

For each detection window:
- The weak classifiers return binary outputs by comparing computed feature values with their respective thresholds, directing the evaluation to either a left or right node.
- The sum of classifier outputs within a stage is compared against a stage threshold to determine whether the window passes the stage.
- If a window successfully passes through all stages, it is classified as containing a face, and its bounding coordinates are stored. Otherwise, it is discarded.

The classifier's parameters, including feature thresholds, node values, and stage thresholds, are learned using the AdaBoost algorithm, which optimally selects and weights weak classifiers to maximize classification accuracy.

# FPGA Implementation of Haar Cascade Classifier

## Pre-requisites

### Haar Features
Haar features are rectangular patterns used to detect important visual characteristics within a given detection window. These features identify intensity differences between adjacent regions, allowing the classifier to recognize key structural elements such as edges, lines, and textures. Each Haar feature is computed by summing pixel intensities in specific regions and comparing them, making it possible to distinguish significant visual patterns efficiently.

### Integral Image
The integral image is a technique used to accelerate Haar feature computation. It allows for rapid summation of pixel values within rectangular regions by transforming the original image into a cumulative summed representation. Using this transformation, any rectangular region's sum can be computed in constant time, significantly enhancing the efficiency of Haar feature evaluation.

### Haar Cascade Classifier Architecture
The Haar Cascade classifier operates by scanning a 24×24 detection window across an image and processing it through multiple sequential stages. Each stage consists of a predefined number of Haar features, where each feature corresponds to a weak classifier. These weak classifiers compute feature values and compare them against learned feature thresholds.

For each detection window:
- The weak classifiers return binary outputs by comparing computed feature values with their respective thresholds, directing the evaluation to either a left or right node.
- The sum of classifier outputs within a stage is compared against a stage threshold to determine whether the window passes the stage.
- If a window successfully passes through all stages, it is classified as containing a face, and its bounding coordinates are stored. Otherwise, it is discarded.

The classifier's parameters, including feature thresholds, node values, and stage thresholds, are learned using the AdaBoost algorithm, which optimally selects and weights weak classifiers to maximize classification accuracy.

## Verilog Implementation

### COE Files
The Verilog implementation of the Haar Cascade classifier relies on several COE (Coefficient) files to store precomputed parameters essential for classification. These files facilitate hardware-based processing by providing integral image data, weak classifier thresholds, and stage-related information:

- **`int_img.coe`**: Stores the four integral image coordinates of one of the three regions in a Haar feature, along with its corresponding weight. This enables efficient feature computation in hardware.
- **`weakclassifiers.coe`**: Contains feature thresholds along with the left and right node values of each weak classifier. These values determine the path taken by each feature evaluation during classification.
- **`stage_info.coe`**: Specifies the starting address and the number of weak classifiers present in each stage. This information is crucial for controlling the sequential evaluation of Haar features through multiple stages in the classifier pipeline.

