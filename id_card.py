from PIL import Image, ImageDraw, ImageFont
import qrcode

def round_corners(image, radius):
    """Create rounded corners with transparency"""
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), image.size], radius, fill=255)
    result = image.copy()
    result.putalpha(mask)
    return result

def generate_id_card(user_data, event_data, datetime, id):
    # Dimensions in pixels (300 DPI)
    card_width = int(2.5 * 300)  # 750px
    card_height = int(3.5 * 300)  # 1050px
    white_section_height = 400
    black_section_height = 150
    card_radius = 40  # Radius for entire card corners

    # Create transparent base image
    card = Image.new('RGBA', (card_width, card_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)

    # Create rounded card background
    card_bg = Image.new('RGBA', (card_width, card_height), (255, 255, 255, 255))
    card_bg = round_corners(card_bg, card_radius)
    
    # White background section
    white_bg = Image.new('RGBA', (card_width, white_section_height), (255, 255, 255, 255))
    card_bg.alpha_composite(white_bg, (0, 0))

    # Black bottom section
    black_bg = Image.new('RGBA', (card_width, black_section_height), (0, 0, 0, 255))
    card_bg.alpha_composite(black_bg, (0, card_height - black_section_height))

    # Background image
    bg = Image.open("assets/background.jpg").convert("RGBA")
    bg = bg.resize((card_width, card_height - white_section_height - black_section_height))
    card_bg.alpha_composite(bg, (0, white_section_height))

    # Profile image
    image_size = 120
    profile_img = Image.open("assets/self.jpg").convert("RGBA").resize((image_size, image_size))
    profile_img = round_corners(profile_img, 20)
    card_bg.alpha_composite(profile_img, (card_width - image_size - 50, 250))

    # QR Code
    qr_size = 200
    qr = qrcode.QRCode(box_size=8, border=1)
    qr.add_data(id)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    qr_img = qr_img.resize((qr_size, qr_size))
    qr_img = round_corners(qr_img, 20)
    card_bg.alpha_composite(qr_img, (card_width - qr_size - 50, 750))

    # Logo
    logo = Image.open("assets/logo.png").convert("RGBA").resize((150, 100))
    logo = round_corners(logo, 20)
    card_bg.alpha_composite(logo, (50, 930))

    # Composite everything onto the rounded card
    card.alpha_composite(card_bg)

    # Font setup
    poppins_bold = ImageFont.truetype('assets/font/Poppins-Bold.ttf', 102)
    poppins_semibold = ImageFont.truetype('assets/font/Poppins-SemiBold.ttf', 38)
    poppins_regular = ImageFont.truetype('assets/font/Poppins-Regular.ttf', 28)
    poppins_medium = ImageFont.truetype('assets/font/Poppins-Medium.ttf', 32)

    # Text positions
    text_positions = {
        'first_name': (46, 45),
        'last_name': (50, 160),
        'designation': (50, 250),
        'host': (50, 300),
        'meeting_room': (50, 340),
        'datetime': (card_width - 200 - 110, 970)
    }

    # Draw text directly on the rounded card
    draw = ImageDraw.Draw(card)
    draw.text(text_positions['first_name'], user_data["first_name"], font=poppins_bold, fill='black')
    draw.text(text_positions['last_name'], user_data["last_name"], font=poppins_semibold, fill='black')
    draw.text(text_positions['designation'], event_data["event_name"], font=poppins_medium, fill='black')
    draw.text(text_positions['host'], f"Host: {event_data['host']}", font=poppins_regular, fill='black')
    draw.text(text_positions['meeting_room'], event_data["place"], font=poppins_regular, fill='black')
    draw.text(text_positions['datetime'], datetime, font=poppins_regular, fill='white')

    # Final composition and save
    final_card = Image.new('RGBA', (card_width, card_height), (255, 255, 255, 255))
    final_card.alpha_composite(card)
    
    # Apply rounded corners to the final composite
    final_card = round_corners(final_card, 40)
    
    # Save as PNG with transparency
    card_name = f"{user_data['first_name']}.png"
    final_card.save(f"assets/cards/{card_name}", dpi=(300, 300))
    print(f"ID Card: {card_name} generated successfully!")


def main():
    generate_id_card(
        user_data={"first_name": "Taufik", "last_name": "Khan"},
        event_data={
            "event_name": "Event 1",
            "host": "Lisa Chan, Stark Sdn Bhd",
            "place": "Meeting Room £, Tower 2, Level 7"
        },
        datetime="14/07/2023  3:25PM",
        id="Zyx12345ABCDE"
    )
    

if __name__ == "__main__":
    main()