import segno
import os
from PIL import Image, ImageDraw, ImageSequence

def create_styled_qr(url, output_filename, background_image, scale=30, opacity=255):
    try:
        # Create QR code with higher error correction
        qr = segno.make(url, error='h')
        matrix = qr.matrix
        
        # Calculate scale to fit 300px
        target_size = 300
        content_size = target_size - 20
        module_count = len(matrix)
        scale = content_size // (module_count + 4)
        
        # Calculate dimensions
        module_size = scale
        quiet_zone = 2
        qr_size = len(matrix) * module_size + 2 * quiet_zone * module_size
        
        # Open and prepare background
        bg = Image.open(background_image)
        
        frames = []
        for frame in ImageSequence.Iterator(bg):
            # Create white background
            base = Image.new("RGBA", (target_size, target_size), (255, 255, 255, 255))
            
            # Resize and center the frame
            frame = frame.convert("RGBA")
            frame = frame.resize((qr_size, qr_size))
            
            # Calculate position to center QR code
            x_offset = (target_size - qr_size) // 2
            y_offset = (target_size - qr_size) // 2
            
            # Paste frame onto white background
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
                        # Large corner squares
                        draw.rectangle(
                            [pos_x-2, pos_y-2, pos_x + module_size+2, pos_y + module_size+2],
                            fill=(255, 255, 255, 255)
                        )
                        draw.rectangle(
                            [pos_x, pos_y, pos_x + module_size, pos_y + module_size],
                            fill=(0, 0, 0, 255)
                        )
                    else:
                        # Small data pixels
                        padding = int(module_size * 0.3)
                        draw.rectangle(
                            [pos_x + padding-1, pos_y + padding-1, 
                             pos_x + module_size - padding+1, pos_y + module_size - padding+1],
                            fill=(255, 255, 255, 255)
                        )
                        draw.rectangle(
                            [pos_x + padding, pos_y + padding, 
                             pos_x + module_size - padding, pos_y + module_size - padding],
                            fill=(0, 0, 0, opacity)
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