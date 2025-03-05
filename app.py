import streamlit as st
import segno
import os
from PIL import Image

def create_artistic_qr(url, background_file, output_filename, scale=6):
    try:
        # Create QR code
        qr = segno.make_qr(url)
        
        # Create temporary PNG QR code
        temp_qr = "temp_qr.png"
        qr.save(temp_qr, scale=scale, dark="black", light=None)
        
        # Process images with PIL
        qr_image = Image.open(temp_qr)
        bg_image = Image.open(background_file)
        
        # Convert to RGBA if needed
        if bg_image.mode != 'RGBA':
            bg_image = bg_image.convert('RGBA')
        if qr_image.mode != 'RGBA':
            qr_image = qr_image.convert('RGBA')
        
        # Resize QR to match background
        qr_image = qr_image.resize(bg_image.size)
        
        # Combine images
        result = Image.alpha_composite(bg_image, qr_image)
        result.save(output_filename)
        
        # Cleanup
        os.remove(temp_qr)
        return True
        
    except Exception as e:
        st.error(f"Error creating QR code: {e}")
        return False

def main():
    # Configure page layout
    st.set_page_config(
        page_title="Sicredi QR Code Generator",
        page_icon="🔗",
        layout="centered"
    )
    # Custom CSS - add these styles
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@400;700&display=swap');
        
        * {
            font-family: 'Exo 2', sans-serif !important;
        }
        .stApp {
            background-color: #f5f5f5;
        }
        .header {
            background-color: #000000;
            padding: 1rem;
            width: 100%;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            padding-left: 2rem;
        }
        .content-box {
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            margin: 5rem auto 4rem auto;
            max-width: 800px;
        }
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #000000;
            color: white;
            text-align: center;
            padding: 1rem;
            font-family: 'Exo 2', sans-serif;
            font-size: 0.9rem;
            z-index: 1000;
        }.whatsapp-button {
            position: fixed;
            bottom: 80px;
            right: 25px;
            background-color: #25D366;
            color: white;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.4);
            z-index: 1000;
            transition: all 0.3s ease;
        }
        .whatsapp-button:hover {
            transform: scale(1.1);
            background-color: #20ba5a;
        }
        .whatsapp-icon {
            font-size: 35px;
        }
        </style>
        <a href="https://wa.me/5565981173624?text=Olá,%20estou%20com%20dúvidas" target="_blank" class="whatsapp-button">
            <svg class="whatsapp-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
                <path fill="white" d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7.9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/>
            </svg>
        </a>
    """, unsafe_allow_html=True)
    # Header with logo
    st.markdown("""
        <div class="header">
            <div class="logo-container">
                <img src="./logo.png" class="logo-img" alt="Sicredi Logo">
            </div>
        </div>
        <div class="footer">© Todos os direitos reservados 2025 Sicredi Grandes Rios MT/PA/AM</div>
    """, unsafe_allow_html=True)
    # Main container with content
    with st.container():
        st.markdown('<h1 class="page-title">QRCode Animado</h1>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    # Main content
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.write("Crie seu QR code animado personalizado")
    
    # URL input with better styling
    url = st.text_input("URL:", "https://www.sicredi.com.br", 
                       help="Digite a URL para seu QR code")
    
    # File uploader with instructions
    uploaded_file = st.file_uploader("Escolha um arquivo GIF", 
                                   type=['gif'],
                                   help="Faça upload de um GIF animado para usar como fundo")
    
    if uploaded_file is not None:
        cols = st.columns(2)
        with cols[0]:
            st.image(uploaded_file, caption="Prévia", use_container_width=True)
        
        with cols[1]:
            if st.button("Gerar QR Code", type="primary"):
                with st.spinner("Criando QR Code..."):
                    output_path = "generated_qr.gif"
                    success = create_artistic_qr(url, uploaded_file, output_path)
                    
                    if success:
                        st.success("QR Code gerado com sucesso!")
                        st.image(output_path, caption="QR Code Gerado")
                        
                        # Styled download button
                        with open(output_path, "rb") as file:
                            st.download_button(
                                label="⬇️ Baixar QR Code",
                                data=file,
                                file_name="qr_code.gif",
                                mime="image/gif"
                            )
                            # Remove the duplicate download button that was here
if __name__ == "__main__":
    main()