from tkinter import filedialog
from PIL import Image, UnidentifiedImageError, ImageDraw, ImageFont, ImageOps

class Watermarker:
    def __init__(self):
        self.base_image = None
        self.watermark_image = None
        self.watermark_text = None
        self.watermark_location = None
        self.mark_is_text = False
        self.mark_is_image = False
        self.text_color = None
    
    def upload_photo(self):
        filename = filedialog.askopenfilename()
        try:
            image = Image.open(filename).convert("RGBA")
            self.base_image = ImageOps.exif_transpose(image)
        except UnidentifiedImageError:
            raise Exception("Sorry, that's not an image file. Only image files may be uploaded.")
        
    def upload_watermark_photo(self):
        filename = filedialog.askopenfilename()
        try:
            watermark_image = Image.open(filename).convert("RGBA")
            self.watermark_image = ImageOps.exif_transpose(watermark_image)
        except UnidentifiedImageError:
            raise Exception("Sorry, that's not an image file. Only image files may be uploaded.")
        else:
            self.mark_is_image = True
            
    def get_text(self, text):
        self.watermark_text = text
        self.mark_is_text = True
    
    def get_location(self, location):
        self.watermark_location = location
        
    def set_mark_location(self, image_width, image_height, mark_width, mark_height):
        margin = 20
        if self.watermark_location == "Center":
            x = (image_width / 2) - (mark_width /2)
            y = (image_height /2) - (mark_height /2)
        elif self.watermark_location == "Top-Left":
            x = margin
            y = margin
        elif self.watermark_location == "Top-Right":
            x = image_width - mark_width - margin
            y = margin
        elif self.watermark_location == "Bottom-Left":
            x = margin
            y = image_height - mark_height - margin
        elif self.watermark_location == "Bottom-Right":
            x = image_width - mark_width - margin
            y = image_height - mark_height - margin
        else:
            raise Exception("Something went wrong - please re-run the application and try again, "
                            "or note the details of the big and notify me.")
        return int(x), int(y)
    
    def mark_image(self):
        image_width, image_height = self.base_image.size
        if self.mark_is_text:
            overlay_image = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 0))
            draw = ImageDraw.Draw(overlay_image)
            text = self.watermark_text
            font_size = int(((image_width + image_height) / 2) // 12)
            font = ImageFont.truetype("segoeui.ttf", font_size)
            mark_width, mark_height = draw.textsize(text, font)
            x, y = self.set_mark_location(image_width, image_height, mark_width, mark_height)
            draw.text((x, y), text, font=font, fill=self.text_color)
            watermarked_image = Image.alpha_composite(self.base_image, overlay_image)
        elif self.mark_is_image:
            mark_image = self.watermark_image
            mark_max_size = (image_width // 4, image_height // 4)
            mark_image.putalpha(32)
            mark_image.thumbnail(mark_max_size)
            mark_width, mark_height = mark_image.size
            x, y = self.set_mark_location(image_width, image_height, mark_width, mark_height)
            self.base_image.paste(mark_image, (x, y), mark_image)
            watermarked_image = self.base_image
        else:
            raise Exception("Something went wrong - please re-run the application and try again, "
                            "or note the details of the bug and notify me.")
        watermarked_image.show()
        watermarked_image.save("watermarked_image.png")