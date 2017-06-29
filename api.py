from flask import Flask, jsonify
from flask import request, redirect, render_template, make_response
from time import time


# FLASK_APP=api.py flask run

app = Flask(__name__)



# para instrucciones paso por paso para llegar de A a B
class lift:
	def __init__(self, identificador):
		self.identificador = identificador

# class run:
# 	def __init__(self, identificador):
# 		self.identificador = identificador
####################################################################

class skier:
	all_skiers = {}
	def __init__(self, card_read):
		self.card_read = card_read
		self.alert = False
		self.last_pos = None
		skier.all_skiers[card_read] = self
		self.group = None
		self.name = None
		self.history = []

	def __repr__(self):
		if self.name:
			return self.name
		return "User card id: " + str(self.card_read)

	def access(self, lift):
		self.history.append(lift, time)


class group:
	current_id = 0
	def __init__(self, first_member):
		self.members = [first_member]
		self.id = group.current_id
		group.current_id += 1

	def add_member(self, member):		# redundante?	
		if member not in self.members:
			self.members.append(member)
		member.group = self				# sobreescribe el grupo antiguo
		print(self.members)


def traducir(numero, ret_object=False):
	if str(bin(int(numero)))[-1]=="1":
		number = 2
	elif str(bin(int(numero)))[-5] == "1":
		number = 3
	else:
		number = 1
	if not number in skier.all_skiers:	# crea nuevos esquiadores automaticamente
		_ = skier(number)
	return skier.all_skiers[number] if ret_object else number

####################################################################


@app.route("/")
def index():
	# main page
	return render_template("main.html")


@app.route('/user')
def show_user():
	yo = skier.all_skiers[int(traducir(request.cookies.get('userID')))]		# si no existe se crea al traducir y luego lo busca
	yo.access("Parvita")
	return render_template("user.html")

@app.route('/user/friends')
def show_friends():
	amigos = []
	yo = skier.all_skiers[int(traducir(request.cookies.get('userID')))]
	if yo.group:
		for index, member in enumerate(yo.group.members):
			if member != yo:
				amigos.append([str(member), member.alert, index])
	else:
		amigos=[]
	return render_template("friends.html",results=amigos)


@app.route('/user/group')
def create_group():
	amigos = []
	yo = skier.all_skiers[int(traducir(request.cookies.get('userID')))]
	if yo.group:
		for member in yo.group.members:
			if member != yo:
				amigos.append([str(member), member.alert])
	else:
		amigos=[]
	return render_template("armar_grupo.html",results=amigos, number=1)


# @app.route('/main/<int:userid>')
# def show_main(userid):
# 	# show the user profile for that user
# 	amigos = ""
# 	active_user = skier.all_skiers[int(userid)]
# 	if active_user.group:
# 		for amigo in active_user.group.members:
# 			amigos += "<p>" + str(amigo) + "  status alert: " + str(amigo.alert) + "</p>"
# 	return """
# <link rel= "stylesheet" type= "text/css" href= "/static/styles/style.css">
# <body background="/static/pantalla.png">
# <h1>agregar amigos</h1>
# <form action="/add_friends" method="post" id="custom-search-form" class="form-search form-horizontal pull-right">
#   <input type="hidden" name="identificador" value="{}">
#   <input type="text" name="identificador_amigo" placeholder="identificador" autofocus></input>
#   """.format(userid) + amigos + """  
#   <img src="/static/pantalla.png" width="1200">
# </form>
# <form action="/alert" method="post">
# 	<input type="hidden" name="identificador" value="{}">
#     <input type="submit" value="ALERT" />
# </form>
# <p>alert status = {}</p>
# </body>
# """.format(userid, active_user.alert)



@app.route('/register', methods=['POST'])
def register():
	# receive card data
	identificador = request.form['identificador']
	print("El numero es '" + identificador + "'")
	resp = make_response(render_template('user.html'))
	resp.set_cookie('userID', identificador)
	return resp


@app.route('/add_friends', methods=['POST'])
def add_friends():
	# recibe id de amigo a agregar
	identificador_amigo = request.form['identificador_amigo']
	identificador = request.cookies.get('userID')
	print("El agregado es '" + str(traducir(identificador_amigo)) + "'")
	print("yo: " + identificador)
	adder = skier.all_skiers[int(traducir(identificador))]
	if not adder.group:
		adder.group = group(adder)
	amigo = traducir(identificador_amigo, True)
	adder.group.add_member(amigo)
	if not amigo.name:
		return redirect('/user/group')		# elegir un nombre
	return redirect('/user/group')


@app.route('/alert')
def alert():
	# recibe solicitud de alerta
	yo = skier.all_skiers[int(traducir(request.cookies.get('userID')))]
	yo.alert = True
	return redirect('user')

@app.route('/friend_history/<int:index>')
def friend_history(index):
	# llamado por friends.html devuelve el indice en la lista de amigos del clickeado
	hora_actual = time()
	posicion_actual = "Parvita"		# asume que todos estan en parvita mientras no haya sistema mas preciso
	return render_template("friend_history.html", results=[(posicion_actual, hora_actual)])


# @app.route('/print_test', methods=['GET', 'POST'])
# def print_test():
# 	# funcion para hacer testing
# 	if request.method == 'POST':
# 		print("POST")
# 		index = request.form['index']
# 		print(index*100)

# 	else: 
# 		print("GET")

# 	yo = skier.all_skiers[int(traducir(request.cookies.get('userID')))]
# 	print(yo.group.members)
# 	print("test ", str(yo))
# 	return redirect('user')


if __name__ == "__main__":
    app.run()