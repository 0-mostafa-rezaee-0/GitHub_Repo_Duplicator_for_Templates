#!/usr/bin/env python3
"""
Icon Generator for GitHub Repo Duplicator.

This script creates a simple icon for the GitHub Repo Duplicator executable.
It requires Pillow (PIL) to be installed.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

def generate_icon():
    """Generate a simple icon for the GitHub Repo Duplicator."""
    # Create a new image with a white background
    img_size = 256
    img = Image.new('RGBA', (img_size, img_size), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a rounded rectangle for the background
    background_color = (0, 121, 203)  # GitHub blue
    draw.rectangle([(10, 10), (img_size-10, img_size-10)], 
                  fill=background_color, width=0)
    
    # Try to find a font, fallback to default if not found
    try:
        # Try to load a font (adjust path as needed for your system)
        font = ImageFont.truetype("arial.ttf", 140)
    except IOError:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw the "GH" text in white
    text = "GH"
    text_color = (255, 255, 255)
    
    # Get text size to center it
    textbbox = draw.textbbox((0, 0), text, font=font)
    text_width = textbbox[2] - textbbox[0]
    text_height = textbbox[3] - textbbox[1]
    
    # Position text in the center
    text_position = ((img_size - text_width) // 2, (img_size - text_height) // 2 - 20)
    draw.text(text_position, text, font=font, fill=text_color)
    
    # Draw a smaller "RD" text for "Repo Duplicator"
    smaller_text = "RD"
    smaller_font_size = 80
    
    try:
        smaller_font = ImageFont.truetype("arial.ttf", smaller_font_size)
    except IOError:
        smaller_font = ImageFont.load_default()
    
    # Position the smaller text below the main text
    smaller_textbbox = draw.textbbox((0, 0), smaller_text, font=smaller_font)
    smaller_text_width = smaller_textbbox[2] - smaller_textbbox[0]
    smaller_text_height = smaller_textbbox[3] - smaller_textbbox[1]
    
    smaller_text_position = ((img_size - smaller_text_width) // 2, 
                             text_position[1] + text_height + 10)
    draw.text(smaller_text_position, smaller_text, font=smaller_font, fill=text_color)
    
    # Save the image to the appropriate directory
    # When running as a module vs. script, the paths will be different
    if '__file__' in globals():
        # Running as a script
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    else:
        # Running as a module
        base_dir = os.path.dirname(os.getcwd())
    
    build_dir = os.path.join(base_dir, 'build', 'pyinstaller')
    os.makedirs(build_dir, exist_ok=True)
    
    icon_path = os.path.join(build_dir, 'github_repo_duplicator_icon.png')
    ico_path = os.path.join(build_dir, 'icon.ico')
    
    img.save(icon_path, 'PNG')
    print(f"Created PNG icon at {icon_path}")
    
    # Convert to ICO format if possible
    try:
        # Create .ico file (for Windows)
        img.save(ico_path, format='ICO', sizes=[(256, 256)])
        print(f"Created ICO icon at {ico_path}")
    except Exception as e:
        print(f"Could not create ICO file: {e}")
        print("You may need to convert the PNG to ICO manually using an online converter.")

def main():
    """Run the icon generator."""
    try:
        generate_icon()
    except ImportError:
        print("Error: This script requires the Pillow library.")
        print("Install it with: pip install pillow")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 