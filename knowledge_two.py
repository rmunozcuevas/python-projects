import qrcode
import qrcode.image.svg

factory = qrcode.image.svg.SvgPathImage

svg_img = qrcode.make("LOCK IN RAYMUNDO", image_factory=factory)
svg_img.save("mygr.svg")

#SVG VECTOR GRAPHICS QR CODE

