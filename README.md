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
