import matplotlib.pyplot as plt
from PIL import Image
img = Image.open('image.jpg')    # Input Image path
gray_img = img.convert('L')  
resized_gray_img = gray_img.resize((24, 24))
resized_gray_img.save('preprocessed_image_plt.png') # Don't change path

plt.imshow(resized_gray_img, cmap='gray')
plt.axis('off')  # Hide axes
plt.title('Resized Grayscale Image')
plt.show()
