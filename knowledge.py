import qrcode
qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,
                   box_size=50,border=2)


qr.add_data("https://webpages.charlotte.edu/rmunozcu/itis3135/homepage.html")
qr.make(fit=True)

img = qr.make_image(fill_color="blue", back_color="white")
img.save("simple.png")

