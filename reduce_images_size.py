import os
from PIL import Image

# Path to the folder containing the images
input_folder = input("Enter the path to the folder containing the images: ")
output_folder = input("Enter the path to the folder to save the resized images: ")

# Make sure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def reduce_image_size(image_path, output_path, scale_factor=0.2):
    """Reduces the image size by the given scale factor."""
    with Image.open(image_path) as img:
        # Calculate new size by reducing by 80%
        new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
        resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Save the resized image
        resized_img.save(output_path)


# Loop through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
        # Construct full file path
        input_file_path = os.path.join(input_folder, filename)
        output_file_path = os.path.join(output_folder, filename)
        
        # Reduce image size and save to output folder
        reduce_image_size(input_file_path, output_file_path)

print(f"All images resized by 80% and saved to {output_folder}.")
