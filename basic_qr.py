import segno
import os
from PIL import Image, ImageDraw, ImageSequence

def create_basic_qr(url, output_filename, background_image, scale=30):
    try:
        qr = segno.make(url, error='h')
        matrix = qr.matrix
        
        # Ajustando dimensões para centralização
        module_size = scale
        quiet_zone = 4
        qr_content_size = len(matrix) * module_size
        qr_total_size = qr_content_size + (2 * quiet_zone * module_size)
        
        # Criar imagem maior para centralizar
        target_size = qr_total_size + (4 * module_size)  # Margem extra aumentada
        
        bg = Image.open(background_image)
        
        frames = []
        for frame in ImageSequence.Iterator(bg):
            frame = frame.convert("RGBA")
            frame = frame.resize((target_size, target_size))
            
            overlay = Image.new("RGBA", frame.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Calculando offset para centralização
            offset_x = (target_size - qr_content_size) // 2
            offset_y = (target_size - qr_content_size) // 2
            
            for y, row in enumerate(matrix):
                for x, cell in enumerate(row):
                    pos_x = x * module_size + offset_x
                    pos_y = y * module_size + offset_y
                    
                    is_finder = (x < 7 and y < 7) or (x < 7 and y >= len(matrix) - 7) or (x >= len(matrix) - 7 and y < 7)
                    
                    if is_finder:
                        # Padrões de localização estilo artístico
                        draw.rectangle(
                            [pos_x-4, pos_y-4, pos_x + module_size+4, pos_y + module_size+4],
                            fill=(255, 255, 255, 255)
                        )
                        draw.rectangle(
                            [pos_x, pos_y, pos_x + module_size, pos_y + module_size],
                            fill=(0, 0, 0, 255)
                        )
                    else:
                        # Pontos pequenos estilo artístico
                        dot_size = int(module_size * 0.3)  # Pontos menores
                        margin = (module_size - dot_size) // 2
                        
                        if cell:  # Pixel preto
                            draw.rectangle(
                                [pos_x + margin, pos_y + margin, 
                                 pos_x + margin + dot_size, pos_y + margin + dot_size],
                                fill=(0, 0, 0, 255)
                            )
                        else:  # Pixel branco/transparente
                            draw.rectangle(
                                [pos_x + margin, pos_y + margin, 
                                 pos_x + margin + dot_size, pos_y + margin + dot_size],
                                fill=(255, 255, 255, 30)  # Ainda mais transparente
                            )
            
            combined = Image.alpha_composite(frame, overlay)
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
    print("Creating basic animated QR code...")
    create_basic_qr(
        'https://www.sicredi.com.br/coop/grandesrios/assembleias-2025/',
        'test_default.gif',
        'sicre.gif',
        scale=30
    )