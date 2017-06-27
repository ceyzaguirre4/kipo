from flask import Flask, jsonify
from flask import request, redirect


# FLASK_APP=api.py flask run

app = Flask(__name__)



# para instrucciones paso por paso para llegar de A a B
# class lift:
# 	def __init__(self, identificador):
# 		self.identificador = identificador

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

	def __repr__(self):
		if self.name:
			return self.name
		return "User card id: " + str(self.card_read)


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
	return """
<link rel= "stylesheet" type= "text/css" href= "/static/styles/style.css">
<body background="/static/pantalla.png">
<form action="/register" method="post" id="custom-search-form" class="form-search form-horizontal pull-right">
  <input type="text" name="identificador" placeholder="identificador" autofocus></input>
</form>
</body>
"""




@app.route('/main/<int:userid>')
def show_main(userid):
	# show the user profile for that user
	amigos = ""
	active_user = skier.all_skiers[int(userid)]
	if active_user.group:
		for amigo in active_user.group.members:
			amigos += "<p>" + str(amigo) + "  status alert: " + str(amigo.alert) + "</p>"
	return """
<link rel= "stylesheet" type= "text/css" href= "/static/styles/style.css">
<body background="/static/pantalla.png">
<h1>agregar amigos</h1>
<form action="/add_friends" method="post" id="custom-search-form" class="form-search form-horizontal pull-right">
  <input type="hidden" name="identificador" value="{}">
  <input type="text" name="identificador_amigo" placeholder="identificador" autofocus></input>
  """.format(userid) + amigos + """  
  <img src="/static/pantalla.png" width="1200">
</form>
<form action="/alert" method="post">
	<input type="hidden" name="identificador" value="{}">
    <input type="submit" value="ALERT" />
</form>
<p>alert status = {}</p>
</body>
""".format(userid, active_user.alert)



@app.route('/register', methods=['GET', 'POST'])
def register():
	# receive card data
	if request.method == 'POST':
		identificador = request.form['identificador']
		print("El numero es '" + identificador + "'")
		return redirect('/main/{}'.format(traducir(identificador)))
	else:
		return "404 register Intente de nuevo"



@app.route('/add_friends', methods=['GET', 'POST'])
def add_friends():
	if request.method == 'POST':
		identificador_amigo = request.form['identificador_amigo']
		identificador = request.form['identificador']
		print("El agregado es '" + str(traducir(identificador_amigo)) + "'")
		print("yo: " + identificador)
		adder = skier.all_skiers[int(identificador)]
		if not adder.group:
			adder.group = group(adder)
		adder.group.add_member(traducir(identificador_amigo, True))
		return redirect('/main/{}'.format(identificador))
	else:
		return "404 add_friends Intente de nuevo"



@app.route('/alert', methods=['GET', 'POST'])
def alert():
	if request.method == 'POST':
		identificador = request.form['identificador']
		print("yo alerta: " + identificador)
		adder = skier.all_skiers[int(identificador)]
		adder.alert = True
		return redirect('/main/{}'.format(identificador))
	else:
		return "404 alert Intente de nuevo"

