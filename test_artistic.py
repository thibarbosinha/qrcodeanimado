import segno

def create_artistic_qr(url, background_image, output_filename, scale=8):
    try:
        # Create single QR code with high error correction
        qr = segno.make(url, error='h')
        
        # Create artistic QR code
        qr.to_artistic(
            background=background_image,
            target=output_filename,
            scale=scale,
            dark='black',
            light=None  # This makes light modules transparent
        )
        
        print(f"QR code saved as {output_filename}")
        return True
        
    except Exception as e:
        print(f"Error creating QR code: {e}")
        return False

if __name__ == "__main__":
    print("Creating artistic QR code...")
    create_artistic_qr(
        'https://www.sicredi.com.br',
        'carna.gif',  # Changed background image
        'test_artistic.gif',
        scale=10
    )
