import segno
from pathlib import Path
import io
import os

# Make sure we have the necessary modules
try:
    import qrcode_artistic
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call(["pip", "install", "qrcode-artistic"])
    import qrcode_artistic

# Create QR code with the Sicredi URL
qr = segno.make('https://www.sicredi.com.br/coop/grandesrios/assembleias-2025/', error='h')

# Use the to_artistic method to create the animated QR code
qr.to_artistic(
    background='sicre.gif',
    target='sicredi_animated_qr.gif',
    scale=10
)

print(f"Animated QR code saved as sicredi_animated_qr.gif")