import segno
import os
from PIL import Image, ImageDraw, ImageSequence

def create_qr_with_pil(url, output_filename, background_image, scale=10, opacity=128):
    """
    Create a QR code and overlay it on a background image using PIL
    
    Args:
        url: The URL to encode in the QR code
        output_filename: The filename to save the QR code to
        background_image: The background image to use
        scale: The size of each QR module in pixels
        opacity: Opacity of QR code (0-255, where 0 is transparent, 255 is opaque)
    """
    print(f"Creating QR code for URL: {url}")
    print(f"Using background image: {background_image}")
    
    # Check if background image exists
    if not os.path.exists(background_image):
        print(f"ERROR: Background image '{background_image}' not found!")
        return False
    
    try:
        # Create basic QR code
        qr = segno.make(url, error='h')
        
        # Get QR code as matrix (list of lists)
        matrix = qr.matrix
        
        # Open background image
        bg = Image.open(background_image)
        
        # Calculate QR code size based on scale
        module_size = scale
        quiet_zone = 4  # Standard quiet zone
        qr_size = len(matrix) * module_size + 2 * quiet_zone * module_size
        
        # Resize background to match QR code size
        bg = bg.resize((qr_size, qr_size))
        bg = bg.convert("RGBA")
        
        # Create a transparent overlay for QR code
        overlay = Image.new("RGBA", bg.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Draw QR code on overlay
        for y, row in enumerate(matrix):
            for x, cell in enumerate(row):
                if cell:  # If cell is dark (1)
                    # Calculate position with quiet zone
                    pos_x = (x + quiet_zone) * module_size
                    pos_y = (y + quiet_zone) * module_size
                    
                    # Draw rectangle for the QR module
                    draw.rectangle(
                        [pos_x, pos_y, pos_x + module_size, pos_y + module_size],
                        fill=(0, 0, 0, opacity)  # Semi-transparent black
                    )
        
        # Combine background and overlay
        result = Image.alpha_composite(bg, overlay)
        
        # Save result
        result.save(output_filename)
        print(f"QR code saved as {output_filename}")
        return True
        
    except Exception as e:
        print(f"Error creating QR code: {e}")
        return False

def create_styled_qr(url, output_filename, background_image, scale=30, opacity=255):
    try:
        # Create QR code with medium error correction for better readability
        qr = segno.make(url, error='m')  # Changed to 'm' for balance
        matrix = qr.matrix
        
        # Calculate scale to fit 300px
        target_size = 300
        content_size = target_size - 20  # Leave 10px border on each side
        module_count = len(matrix)
        scale = content_size // (module_count + 4)  # 4 for quiet zone
        
        # Calculate dimensions
        module_size = scale
        quiet_zone = 2
        qr_size = len(matrix) * module_size + 2 * quiet_zone * module_size
        
        # Open and prepare background - Moved here from outside
        bg = Image.open(background_image)
        frames = []
        for frame in ImageSequence.Iterator(bg):
            # Increase white background opacity for better contrast
            base = Image.new("RGBA", (target_size, target_size), (255, 255, 255, 220))
            
            # Resize and center the frame
            frame = frame.convert("RGBA")
            frame = frame.resize((qr_size, qr_size))
            
            # Calculate position to center QR code
            x_offset = (target_size - qr_size) // 2
            y_offset = (target_size - qr_size) // 2
            
            # Paste frame onto semi-transparent background
            base.paste(frame, (x_offset, y_offset))
            
            overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Draw QR code elements
            for y, row in enumerate(matrix):
                for x, cell in enumerate(row):
                    if not cell:
                        continue
                    
                    pos_x = (x + quiet_zone) * module_size + x_offset
                    pos_y = (y + quiet_zone) * module_size + y_offset
                    
                    is_finder = (x < 7 and y < 7) or (x < 7 and y >= len(matrix) - 7) or (x >= len(matrix) - 7 and y < 7)
                    
                    if is_finder:
                        # Make finder patterns more prominent
                        draw.rectangle(
                            [pos_x-3, pos_y-3, pos_x + module_size+3, pos_y + module_size+3],
                            fill=(255, 255, 255, 255)  # Fully opaque white border
                        )
                        draw.rectangle(
                            [pos_x, pos_y, pos_x + module_size, pos_y + module_size],
                            fill=(0, 0, 0, 255)  # Solid black
                        )
                    else:
                        # Slightly larger data pixels
                        padding = int(module_size * 0.35)  # Reduced padding for larger pixels
                        draw.rectangle(
                            [pos_x + padding-1, pos_y + padding-1, 
                             pos_x + module_size - padding+1, pos_y + module_size - padding+1],
                            fill=(255, 255, 255, 255)  # Fully opaque white background
                        )
                        draw.rectangle(
                            [pos_x + padding, pos_y + padding, 
                             pos_x + module_size - padding, pos_y + module_size - padding],
                            fill=(0, 0, 0, 255)  # Fully opaque black pixels
                        )
            
            combined = Image.alpha_composite(base, overlay)
            frames.append(combined)
        
        # Save animated GIF
        frames[0].save(
            output_filename,
            save_all=True,
            append_images=frames[1:],
            optimize=False,
            duration=50,
            loop=0
        )
        print(f"QR code saved as {output_filename}")
        return True
        
    except Exception as e:
        print(f"Error creating QR code: {e}")
        return False

if __name__ == "__main__":
    print("Creating animated QR code...")
    create_styled_qr(
        'https://www.sicredi.com.br/coop/grandesrios/assembleias-2025/',
        'animated_qr_300px.gif',
        'sicre.gif',
        opacity=255
    )