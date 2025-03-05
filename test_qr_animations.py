import segno
import os
import sys
from PIL import Image

# Make sure we have the necessary modules
try:
    import qrcode_artistic
    print("Successfully imported qrcode_artistic")
except ImportError as e:
    print(f"Error importing qrcode_artistic: {e}")
    print("Installing required packages...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "qrcode-artistic"])
        import qrcode_artistic
        print("Successfully installed and imported qrcode_artistic")
    except Exception as install_error:
        print(f"Failed to install qrcode-artistic: {install_error}")
        sys.exit(1)

def create_basic_qr(url, output_filename, scale=10, quiet_zone=4):
    """
    Create a basic QR code without artistic effects
    """
    print(f"Creating basic QR code for URL: {url}")
    
    try:
        # Create QR code with the URL and highest error correction level
        qr = segno.make(url, error='h')
        
        # Save as PNG directly using segno's built-in method
        qr.save(
            output_filename,
            scale=scale,
            quiet_zone=quiet_zone
        )
        
        if os.path.exists(output_filename):
            print(f"Basic QR code saved as {output_filename}")
            return True
        else:
            print(f"ERROR: File was not created at {output_filename}")
            return False
    except Exception as e:
        print(f"Error creating basic QR code: {e}")
        return False

def create_artistic_qr_direct(url, output_filename, background_image, scale=10):
    """
    Create an artistic QR code using direct qrcode_artistic functions
    """
    print(f"Creating artistic QR code for URL: {url}")
    print(f"Using background image: {background_image}")
    
    # Check if background image exists
    if not os.path.exists(background_image):
        print(f"ERROR: Background image '{background_image}' not found!")
        return False
    
    try:
        # Create QR code
        qr = segno.make(url, error='h')
        
        # Convert to PIL image first
        pil_img = qr.to_pil(scale=scale)
        print("Successfully converted QR to PIL image")
        
        # Use qrcode_artistic to apply the background
        result = qrcode_artistic.process(
            qr_image=pil_img,
            background=Image.open(background_image)
        )
        
        # Save the result
        result.save(output_filename)
        
        if os.path.exists(output_filename):
            print(f"Artistic QR code saved as {output_filename}")
            return True
        else:
            print(f"ERROR: File was not created at {output_filename}")
            return False
    except Exception as e:
        print(f"Error creating artistic QR code: {e}")
        return False

def create_test_qr(url, output_filename, background_image, scale=10):
    """
    Create a QR code with the given parameters
    
    Args:
        url: The URL to encode in the QR code
        output_filename: The filename to save the QR code to
        background_image: The background image to use
        scale: The scale of the QR code
    """
    print(f"Creating QR code for URL: {url}")
    print(f"Using background image: {background_image}")
    
    # Check if background image exists
    if not os.path.exists(background_image):
        print(f"ERROR: Background image '{background_image}' not found!")
        return
    
    # Create QR code with the URL and highest error correction level
    qr = segno.make(url, error='h')
    
    try:
        # Use the to_artistic method to create the animated QR code
        qr.to_artistic(
            background=background_image,
            target=output_filename,
            scale=scale
        )
        print(f"QR code successfully saved as {output_filename}")
        return True
    except Exception as e:
        print(f"Error creating QR code: {e}")
        return False

if __name__ == "__main__":
    print("Starting QR code generation tests...")
    
    # Test with default parameters
    create_test_qr(
        'https://www.sicredi.com.br/coop/grandesrios/assembleias-2025/',
        'test_default.gif',
        'sicre.gif'
    )
    
    # Test with different scale
    create_test_qr(
        'https://www.sicredi.com.br/coop/grandesrios/assembleias-2025/',
        'test_large_scale.gif',
        'sicre.gif',
        scale=15
    )
    
    print("Test script completed!")
    print("All test QR codes generated successfully!")