from flask import Flask, render_template, request
from DBcm import UseDatabase

app = Flask(__name__)

app.config['dbconfig'] = {'host': '127.0.0.1', 'user': 'souvik', 'database': 'New', }

def log_request(req: 'flask_request') -> None:
    with UseDatabase(app.config['dbconfig'])as cursor:
        _SQL = """insert into log (name,email,password,mobile,dob,gender,address,ip,browser)
         values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(_SQL, (request.form['name'], request.form['email'], request.form['pass'],
                              request.form['mobile'],request.form['dob'], request.form['gender'],
                              request.form['address'], request.remote_addr, req.user_agent.browser))

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html')


@app.route('/form')
def form() -> 'html':
    return render_template('form.html')


@app.route('/results', methods=['POST'])
def results() -> 'html':
    name = request.form['name']
    log_request(request)
    return render_template('results.html', the_name=name, )

@app.route('/viewlog')
def view_the_log()->'html':
    with UseDatabase(app.config['dbconfig'])as cursor:
        _SQL="""select id,ts,name,email,password,mobile,dob,gender,address,ip,browser from log"""
        cursor.execute(_SQL)
        contents=cursor.fetchall()
    titles=('Sl.No','Time','Name','Email','Password','Contact No','D.O.B','Gender','Address','IP','Browser')
    return render_template('viewlog.html',the_title='View Log',the_row_titles=titles,the_data=contents,)

@app.route('/results', methods=['POST'])
def results() -> 'html':
    return render_template('entry.html')
    name = request.form['name']
    log_request(name)
    return render_template('login.html', pass=pswd, )


if __name__ == '__main__':
    app.run(debug=True)
