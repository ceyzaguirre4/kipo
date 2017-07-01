from PIL import Image
from os import listdir

def generate_map(coord1, identificador_lift):
	if "generated{}.png".format(identificador_lift) in listdir("./static/generated/"):
		return
	background = Image.open("./static/mapa.png")
	foreground = Image.open("./static/pin.png")
	background.paste(foreground, coord1, foreground)
	background.save("./static/generated/generated{}.png".format(identificador_lift))


if __name__ == "__main__":
	generate_map((740, 165), 1)
	print("end.")
