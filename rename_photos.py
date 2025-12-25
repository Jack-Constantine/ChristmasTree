import os
import shutil
import sys

# Try to import Pillow, if not available, warn user
try:
    from PIL import Image
except ImportError:
    print("Error: Pillow library is not installed.")
    print("Please install it using: pip install Pillow")
    sys.exit(1)

def process_images(directory):
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return

    # Get all files
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Filter for images
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}
    images = [f for f in files if os.path.splitext(f)[1].lower() in image_extensions]
    
    if not images:
        print("No images found in the directory.")
        return

    # Sort images to maintain a consistent order (e.g., by name)
    images.sort()
    
    print(f"Found {len(images)} images. Processing...")
    
    # Create a temporary directory to store processed images
    temp_dir = os.path.join(directory, "temp_processing_renaming")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    success_count = 0
    
    for i, filename in enumerate(images, 1):
        file_path = os.path.join(directory, filename)
        new_filename = f"{i}.png"
        temp_path = os.path.join(temp_dir, new_filename)
        
        try:
            with Image.open(file_path) as img:
                # Convert to RGB if necessary (e.g. for some JPEGs or Palette modes)
                if img.mode in ('CMYK', 'P'):
                    img = img.convert('RGB')
                
                img.save(temp_path, 'PNG')
                success_count += 1
                print(f"Processed: {filename} -> {new_filename}")
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

    # If we processed files successfully, replace the originals
    if success_count > 0:
        print("Replacing original files with new files...")
        
        # Remove original images that were in our list
        for filename in images:
            file_path = os.path.join(directory, filename)
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error removing original file {filename}: {e}")

        # Move new files from temp to directory
        for filename in os.listdir(temp_dir):
            src = os.path.join(temp_dir, filename)
            dst = os.path.join(directory, filename)
            shutil.move(src, dst)
            
        print("Done.")
    else:
        print("No files were successfully processed.")
    
    # Cleanup temp dir
    if os.path.exists(temp_dir):
        os.rmdir(temp_dir) # rmdir only works if empty, but we moved everything. 
                           # If move failed, we might have leftovers, so rmtree is safer?
                           # But we expect it to be empty.
        pass

if __name__ == "__main__":
    target_dir = r"c:\Users\Jack1\Desktop\test\christmas_test\ChristmasTree\photos"
    process_images(target_dir)
