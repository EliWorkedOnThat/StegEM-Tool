def user_driven_watermarking(image_path, output_folder):
    """
    Add a user-defined text watermark to an image.
    Prompts the user for customization options such as text, position, opacity, and font size.
    """
    from PIL import Image, ImageDraw, ImageFont
    import os

    print("[DEBUG] Starting user_driven_watermarking...")
    print(f"[DEBUG] Input image path: {image_path}")
    print(f"[DEBUG] Output folder path: {output_folder}")

    # Step 1: Ask for watermark text
    watermark_text = input("Enter the text for the watermark: ").strip()
    print(f"[DEBUG] Watermark text: {watermark_text}")

    # Step 2: Get position preference
    position_choice = input("Do you want to specify the position of the watermark? (Y/N): ").strip().upper()
    if position_choice == "Y":
        x = int(input("Enter the X-coordinate (horizontal position): "))
        y = int(input("Enter the Y-coordinate (vertical position): "))
        position = (x, y)
    else:
        print("Default position (10, 10) will be used.")
        position = (10, 10)
    print(f"[DEBUG] Watermark position: {position}")

    # Step 3: Get opacity preference
    opacity = int(input("Enter the opacity of the watermark (0-255, where 0 is fully transparent): ").strip())
    if not 0 <= opacity <= 255:
        print("Invalid opacity value. Defaulting to 128.")
        opacity = 128
    print(f"[DEBUG] Watermark opacity: {opacity}")

    # Step 4: Get font size preference
    font_size = int(input("Enter the font size for the watermark (e.g., 30): ").strip())
    if font_size <= 0:
        print("Invalid font size. Defaulting to 30.")
        font_size = 30
    print(f"[DEBUG] Watermark font size: {font_size}")

    try:
        # Open the image
        print(f"[DEBUG] Attempting to open image: {image_path}")
        image = Image.open(image_path).convert("RGBA")
        print(f"[DEBUG] Image opened successfully. Size: {image.size}, Mode: {image.mode}")

        txt_overlay = Image.new("RGBA", image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_overlay)

        # Load the font; fall back to default if "arial.ttf" is unavailable
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
            print("[DEBUG] Loaded custom font: arial.ttf")
        except IOError:
            print("[DEBUG] Custom font 'arial.ttf' not found. Using default font.")
            font = ImageFont.load_default()

        # Add the watermark
        draw.text(position, watermark_text, fill=(255, 255, 255, opacity), font=font)
        watermarked_image = Image.alpha_composite(image, txt_overlay)
        print("[DEBUG] Watermark applied to image.")

        # Ensure the destination folder exists
        print(f"[DEBUG] Checking if output folder exists: {output_folder}")
        if not os.path.exists(output_folder):
            print(f"[DEBUG] Folder does not exist. Creating folder: {output_folder}")
            os.mkdir(output_folder)
        else:
            print(f"[DEBUG] Folder already exists: {output_folder}")

        # Save the watermarked image
        output_path = os.path.abspath(os.path.join(output_folder, "watermarked_image.png"))
        print(f"[DEBUG] Attempting to save watermarked image at: {output_path}")
        watermarked_image.convert("RGB").save(output_path, "PNG")

        # Verify that the image was saved successfully
        if os.path.exists(output_path):
            print(f"Watermarked image saved successfully at: {output_path}")
        else:
            print(f"[DEBUG] Failed to save the watermarked image at: {output_path}")

    except Exception as e:
        print(f"[DEBUG] An error occurred while creating the watermark: {e}")
