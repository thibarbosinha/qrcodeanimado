import os

def check_qr_files():
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    print("\nChecking for QR code files:")
    
    files_to_check = ['test_default.gif', 'test_large_scale.gif', 'sicre.gif']
    
    for filename in files_to_check:
        file_path = os.path.join(current_dir, filename)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"\nFound: {filename}")
            print(f"Size: {size} bytes")
            print(f"Full path: {file_path}")
        else:
            print(f"\nNot found: {filename}")

if __name__ == "__main__":
    check_qr_files()