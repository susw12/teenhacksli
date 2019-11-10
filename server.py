import flask, sys, logging, random
from flask import render_template, request, jsonify, Flask, make_response, redirect
import db_methods as db

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

ID_LEN = 100

### Head - done

def genID(id_len = ID_LEN, l = []):
    while True:
        s = ''
        for i in range(id_len):
            t = random.randint(0,2)
            if (t == 0):
                s += chr(ord('0') + random.randint(0, 9))
            elif (t == 1):
                s += chr(ord('a') + random.randint(0, 25))
            else:
                s += chr(ord('A') + random.randint(0, 25))
        if (s not in l):
            l.append(s)
            return s

app = Flask(__name__,
            static_url_path='', 
            static_folder='./public',
            template_folder='./public')
			
### Add product page - progress

# Send HTML, process form progress
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
	if (request.method == 'GET'):
		res = make_response(render_template('add_product.html'))
		return res
	else:
		type = request.cookies.get('type')
		if (not type or type != 'company'):
			return redirect('/invalid_company')
			
		name = request.form['name']
		price = request.form['price']
		desc = request.form['desc']
		tag = request.form['tag']
		
		id = request.cookies.get('id')
		
		db.add_product(price, name, tag, desc, id)
		print("add_product", price, name, tag, desc, id)
		
		# later add no back button - https://stackoverflow.com/questions/20652784/flask-back-button-returns-to-session-even-after-logout
		return redirect('/add_product')

# Get list of tags await aaron
@app.route('/product_tags', methods=['GET'])
def product_tags():
	tags = db.get_tags('')
	return jsonify({'tags': tags})

### Register/login progress

@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
	if (request.method == 'GET'):
		return render_template('register_student.html')
	else:
		uname = request.form['uname']
		pword = request.form['pword']
		name = request.form['name']
		university = request.form['university']
		county = request.form['county']
		zip = request.form['zip']
		state = request.form['state']
		
		rows = db.student_login(uname, pword)
		if (len(rows) == 0):
			db.add_student(name, uname, pword, university, zip, county, state)
			print('register student', name, uname, pword, university, zip, county, state)
			
			rows = db.student_login(uname, pword)

			res = make_response('ok')	
	
			res.set_cookie('id', rows[0][0])

			res.set_cookie('type', 'student')
			return res
		else:
			return 'Account already exists!'
		
@app.route('/register_company', methods=['GET', 'POST'])
def register_company():
	if (request.method == 'GET'):
		return render_template('register_company.html')
	else:
		uname = request.form['uname']
		pword = request.form['pword']
		name = request.form['name']
		phone = request.form['phone']
		email = request.form['email']
		county = request.form['county']
		zip = request.form['zip']
		state = request.form['state']
		
		rows = db.company_login(uname, pword)
		if (len(rows) == 0):
			db.add_company(name, uname, pword, phone, email, zip, county, state)
			print('register company', name, uname, pword, phone, email, zip, county, state)
			
			rows = db.company_login(uname, pword)

			res = make_response('ok')
			res.set_cookie('id', rows[0][0])
			res.set_cookie('type', 'company')
			return res
		else:
			return 'Account already exists!'

@app.route('/login_student', methods=['GET', 'POST'])
def login_student():
	if (request.method == 'GET'):
		return render_template('login_student.html')
	else:
		uname = request.form['uname']
		pword = request.form['pword']
		
		rows = db.student_login(uname, pword)
		
		if (len(rows) == 0):
			print('login student doesnt exist', uname, pword)
			return 'Account does not exist!'
		else:
			res = make_response('ok')
			res.set_cookie('id', rows[0][0])
			res.set_cookie('type', 'student')
			print('login student', uname, pword)
			return res

@app.route('/login_company', methods=['GET', 'POST'])
def login_company():
	if (request.method == 'GET'):
		return render_template('login_company.html')
	else:
		uname = request.form['uname']
		pword = request.form['pword']
		
		rows = db.company_login(uname, pword)
		
		if (len(rows) == 0):
			print('login company doesnt exist', uname, pword)
			return 'Account does not exist!'
		else:
			res = make_response('ok')
			res.set_cookie('id', rows[0][0])
			res.set_cookie('type', 'company')
			print('login company', uname, pword)
			return res

@app.route('/get_student_info', methods=['GET'])
def get_student_info():
	id = request.cookies.get('id')
	student = db.get_student(id)
	return jsonify({'student': student})

@app.route('/update_student', methods=['GET', 'POST'])
def update_student():
	if (request.method == 'GET'):
		return render_template('update_student.html')
	else:
		id = request.cookies.get('id')
		uname = request.form['uname']
		pword = request.form['pword']
		name = request.form['name']
		university = request.form['university']
		county = request.form['county']
		zip = request.form['zip']
		state = request.form['state']

		db.change_student(id, name, uname, pword, university, zip, county, state)
		print('update student', name, uname, pword, university, zip, county, state)
		
		return 'ok'

@app.route('/get_company_info', methods=['GET'])
def get_company_info():
	id = request.cookies.get('id')
	company = db.get_company(id)
	return jsonify({'company': company})

@app.route('/update_company', methods=['GET', 'POST'])
def update_company():
	if (request.method == 'GET'):
		return render_template('update_company.html')
	else:
		id = request.cookies.get('id')
		uname = request.form['uname']
		pword = request.form['pword']
		name = request.form['name']
		phone = request.form['phone']
		email = request.form['email']
		county = request.form['county']
		zip = request.form['zip']
		state = request.form['state']
		
		db.change_company(id, name, uname, pword, phone, email, zip, county, state)
		print('change company', name, uname, pword, phone, email, zip, county, state)

		return 'ok'

### Student hub await sujay

# Send HTML done
@app.route('/student_hub')
def student_hub():
	res = make_response(render_template('student_hub.html'))
	
	type = request.cookies.get('type')
	if (not type or type != 'student'):
		return redirect('/invalid_student')
	return res

@app.route('/student_group', methods=['GET'])
def student_group():
	id = request.cookies.get('id')
	student = db.get_student(id)
	gid = student[-1]
	return gid

@app.route('/create_group', methods=['POST'])
def create_group():
	id = request.cookies.get('id')
	name = request.form['name']
	gid = db.create_group(name)

	db.set_group(id, gid)

	return 'ok'

@app.route('/join_group', methods=['POST'])
def join_group():
	id = request.cookies.get('id')
	gid = request.form['id']

	db.set_group(id, gid)

	return 'ok'

# Get announcements await aaron
@app.route('/list_announcements', methods=['GET'])
def list_announcements():
	type = request.cookies.get('type')
	if (not type or type != 'student'):
		return redirect('/invalid_student')
	
	id = request.cookies.get('id')
	student = db.get_student(id)
	gid = student[-1]
	
	list = db.get_announcement(gid)
	
	return jsonify({'announcements': list})

@app.route('/put_announcement', methods=['POST'])
def put_announcement():
	id = request.cookies.get('id')
	student = db.get_student(id)
	gid = student[-1]
	content = request.form['content']

	db.create_announcement(gid, content)

	return 'ok'
	
@app.route('/list_recipes', methods=['GET'])
def list_recipes():
	query = request.args.get('query')
	
	print('get recipes', query)
	
	recipes = get_recipes(query)
	
	return jsonify({'recipes': recipes})

# 
	
# def get_recipes(query):
	
### Get products page

# @app.route('/product_list', methods=['GET'])
# def product_list():
	# query = request.args.get('something')
	
# def get_products():
	# return [
		# ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'],
		# ['dwa', 'dwa', 'fqwasd', 'fwa', 'wad3qy', 't2qfwas', '2gtqwf', 'y2gew', '54jher']
	# ]

### Invalid pages

@app.route('/invalid_student')
def invalid_student():
	return 'Invalid request, you are not a student'
	
@app.route('/invalid_company')
def invalid_company():
	return 'Invalid request, you are not a company'
	
### Run
		
if __name__ == "__main__":
	app.run(host = 'localhost', port = 4054)