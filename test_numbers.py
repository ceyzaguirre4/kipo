# archivo = open("numbers.txt")
# for line in archivo.readlines():
# 	line = line.strip()
# 	if line:
# 		print(line, str(bin(int(line)))[2:])
# 	else:
# 		print("#"*30)

# while True:
numero = input("acerque tarjeta: ")
print("procesando")
if str(bin(int(numero)))[-1]=="1":
	print("numero2")
elif str(bin(int(numero)))[-5] == "1":
	print("numero3")
else:
	print("numero1")
