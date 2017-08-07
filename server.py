from flask import Flask, session, request, redirect, render_template
import random
import datetime

app = Flask(__name__)

app.secret_key = 'd41d8cd98f00b204e9800998ecf8427e'

@app.route('/')
def index():
    if 'new_gold' not in session:
        session['new_gold'] = 0

    if 'purse' not in session:
        session['purse'] = 0
    else:
        session['purse'] += session['new_gold']
    
    if 'activity' not in session:
        session['activity'] = 'None'
    
    if 'list' not in session:
        session['list'] = []
    
    lst = session['list']
    lst.append(session['activity'])
    session['list'] = lst

    print session['list']

    return render_template('index.html', purse=session['purse'])


@app.route('/process', methods=['POST'])
def process():

    session['time'] = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    session['color'] = 'green'

    if request.form['process'] == 'farm':
        session['new_gold'] = int(random.randrange(9, 21))
        session['activity'] = 'Earned ' + str(session['new_gold']) + ' pieces of gold from the Farm. ' + str(session['time'])    
    elif request.form['process'] == 'cave':
        session['new_gold'] = int(random.randrange(4, 11))
        session['activity'] = 'Earned ' + str(session['new_gold']) + ' pieces of gold from the Cave. ' + str(session['time'])            
    elif request.form['process'] == 'house':
        session['new_gold'] = int(random.randrange(1, 6))
        session['activity'] = 'Earned ' + str(session['new_gold']) + ' pieces of gold from the House. ' + str(session['time'])                
    else:
        session['new_gold'] = int(random.randrange(-51, 51))
        if int(session['new_gold']) < 0:
            session['activity'] = 'Entered a Casino and lost ' + str(session['new_gold']) + ' pieces of gold... Ouch. ' +  str(session['time'])
        else:
            session['activity'] = 'Earned ' + str(session['new_gold']) + ' pieces of gold from the Casino. ' + str(session['time'])    
        
    print request.form['process']
    
    return redirect('/')

@app.route('/reset', methods=['Post'])
def reset():
    session.clear()

    return redirect('/')

app.run(debug=True)