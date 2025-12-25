import os
from PIL import Image

def convert_images(source_dir, dest_dir, max_size=1536):
    # Ensure destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Created directory: {dest_dir}")

    # Get all PNG files
    files = [f for f in os.listdir(source_dir) if f.lower().endswith('.png')]
    
    if not files:
        print(f"No .png files found in {source_dir}")
        return

    print(f"Found {len(files)} PNG files. Processing...")

    for filename in files:
        file_path = os.path.join(source_dir, filename)
        # Construct new filename with .webp extension
        name_without_ext = os.path.splitext(filename)[0]
        new_filename = f"{name_without_ext}.webp"
        dest_path = os.path.join(dest_dir, new_filename)

        try:
            with Image.open(file_path) as img:
                # Check dimensions and resize if necessary
                width, height = img.size
                if width > max_size or height > max_size:
                    # Calculate aspect ratio preserving resize
                    if width > height:
                        new_width = max_size
                        new_height = int(height * (max_size / width))
                    else:
                        new_height = max_size
                        new_width = int(width * (max_size / height))
                    
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    print(f"Resized {filename}: {width}x{height} -> {new_width}x{new_height}")
                
                # Save as WebP
                img.save(dest_path, 'WEBP', quality=80)
                print(f"Converted: {filename} -> {new_filename}")
                
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

    print("Conversion complete.")

if __name__ == "__main__":
    # Define paths relative to the script location or absolute
    base_dir = os.path.dirname(os.path.abspath(__file__))
    source_directory = os.path.join(base_dir, "photos")
    destination_directory = os.path.join(base_dir, "photos_webp")
    
    convert_images(source_directory, destination_directory)
