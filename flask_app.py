from flask import Flask, jsonify
from flask import request, redirect, render_template, make_response
from time import time
from datetime import timedelta


# todo: falta hacer el focus constante en safari !!!
# todo: falta hacer pagina de cambio de nombre
# todo: boton de agregar persona en vez de espacio en armar_grupo.html
# todo: alert en user
# todo: alert cuando se manda mensaje


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
		self.alert_responded = False

	def __repr__(self):
		# if self.name:
		# 	return self.name
		# return "User card id: " + str(self.card_read)
		if self.card_read == 1:
			return "Fran"
		elif self.card_read == 2:
			return "Ale"
		else:
			return "Jose"

	def access(self, lift):
		self.history.append((lift, time()))
		print("acceso")
		print(self.history)


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
	yo = skier.all_skiers[int(traducir(request.cookies.get('userID')))]
	responded = yo.alert_responded
	print(responded)
	yo.alert_responded = False
	return render_template("user.html", response=responded)


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


@app.route('/register', methods=['POST'])
def register():
	# receive card data
	identificador = request.form['identificador']
	print("El numero es '" + identificador + "'")
	#resp = make_response(render_template('user.html'))
	resp = redirect("/user")
	resp.set_cookie('userID', identificador)
	yo = skier.all_skiers[int(traducir(identificador))]		# si no existe se crea al traducir y luego lo busca
	yo.access(request.cookies.get('posicion'))
	# if not yo.name:													# ojo, que devuelva cookie
	# 	return render_template("user.html")
	# 	return redirect('elegir_nombre/{}'.format(yo.card_read))		# elegir un nombre
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
	amigo.access(request.cookies.get('posicion'))
	adder.group.add_member(amigo)
	if not amigo.name:
		return redirect('/user/group')
		return redirect('elegir_nombre/{}'.format(amigo.card_read))		# elegir un nombre
	return redirect('/user/group')


@app.route('/alert')
def alert():
	# recibe solicitud de alerta
	yo = skier.all_skiers[int(traducir(request.cookies.get('userID')))]
	yo.alert = True
	return redirect('user')


@app.route('/voy/<int:identifier>')
def voy(identifier):
	# cuando el usuario se compromete a ir a buscar al alertador.
	hora_actual = time()
	yo = skier.all_skiers[int(traducir(request.cookies.get('userID')))]
	friend = skier.all_skiers[int(identifier)]
	ultima_posicion, hora = friend.history[-1]
	alertador = friend.card_read
	friend.alert = False						# ya no sale alert !!!
	friend.alert_responded = True
	if ultima_posicion: 
		return render_template("friend_history.html", results=[(ultima_posicion, timedelta(seconds=int(hora_actual-hora)))], nombre=str(friend), alertador=alertador, alert=friend.alert)
	else:		# por si se les olvida hacer el set_location
		return render_template("friend_history.html", results=[("Parvita", timedelta(seconds=int(hora_actual-hora)))], nombre=str(friend), alertador=alertador, alert=friend.alert)


@app.route('/friend_history/<int:index>')
def friend_history(index):
	# llamado por friends.html devuelve el indice en la lista de amigos del clickeado
	hora_actual = time()
	yo = skier.all_skiers[int(traducir(request.cookies.get('userID')))]
	friend = yo.group.members[int(index)]
	ultima_posicion, hora = friend.history[-1]
	alertador = friend.card_read
	if ultima_posicion: 
		return render_template("friend_history.html", results=[(ultima_posicion, timedelta(seconds=int(hora_actual-hora)))], nombre=str(friend), alertador=alertador, alert=friend.alert)
	else:		# por si se les olvida hacer el set_location
		return render_template("friend_history.html", results=[("Parvita", timedelta(seconds=int(hora_actual-hora)))], nombre=str(friend), alertador=alertador, alert=friend.alert)


@app.route('/elegir_nombre/<int:identifier>')
def elegir_nombre(identifier):
	esquiador = skier.all_skiers[int(identifier)]
	return "choose name"


@app.route('/set_location/<location>')
def set_location(location):
	resp = make_response(render_template('main.html'))
	resp.set_cookie('posicion', location)
	return resp


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
    # app.run(host='127.0.0.1',port=8000,debug=True)