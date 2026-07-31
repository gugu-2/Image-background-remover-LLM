import os
from rembg import remove

def process_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    images_processed = False
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            images_processed = True
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + '_nobg.png'
            output_path = os.path.join(output_folder, output_filename)
            
            print(f"Processing {filename}...")
            
            try:
                with open(input_path, 'rb') as i:
                    with open(output_path, 'wb') as o:
                        input_data = i.read()
                        # Removing background
                        output_data = remove(input_data)
                        o.write(output_data)
                print(f"Saved to {output_filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                
    if not images_processed:
        print(f"No images found in '{input_folder}'. Please add some images (.jpg, .png, .webp) and try again.")

if __name__ == "__main__":
    input_dir = "input_images"
    output_dir = "output_images"
    
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print(f"Created '{input_dir}' folder. Please add your images there and run the script again.")
    else:
        print("Starting background removal process...")
        process_images(input_dir, output_dir)
        print("Done!")
