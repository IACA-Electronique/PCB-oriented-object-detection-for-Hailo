from PIL import Image
import os
import argparse

def resize_images(source_dir, target_dir, size=(640, 640)):
    """
    Resize all images in the source directory to the specified size and save them to the target directory.

    Args:
        source_dir (str): Path to the directory containing the images to resize.
        target_dir (str): Path to the directory where resized images will be saved.
        size (tuple): Target size as (width, height). Default is (640, 640).
    """
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return

    # Create the target directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Loop through all files in the source directory
    for filename in os.listdir(source_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            try:
                # Open the image file
                img_path = os.path.join(source_dir, filename)
                img = Image.open(img_path)

                # Resize the image
                img_resized = img.resize(size, Image.LANCZOS)

                # Save the resized image to the target directory
                target_path = os.path.join(target_dir, filename)
                img_resized.save(target_path)

                print(f"Resized and saved: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize images in a directory.")
    parser.add_argument("source_dir", help="Path to the directory containing the images to resize.")
    parser.add_argument("output_dir", help="Path to the directory where resized images will be saved.")
    
    args = parser.parse_args()

    resize_images(args.source_dir, args.output_dir)