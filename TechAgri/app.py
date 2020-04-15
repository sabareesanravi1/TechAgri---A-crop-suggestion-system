


from flask import Flask, render_template
from flask import Flask, request, render_template, send_from_directory
import os
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
from werkzeug import secure_filename
import cgi, cgitb
import itertools
app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
app.config['MONGO_DBNAME'] = 'agri'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/agri'
app.config['UPLOAD_FOLDER']='E:\techagr\static'
app.secret_key = '1234'
mongo = PyMongo(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def page():
    return render_template('home.html')

@app.route('/homepage')
def homepage():
    return render_template('home1.html')

@app.route('/login')
def message():
    return render_template('login.html')    

@app.route('/logged',methods=['POST'])
def message2():
    return render_template('home1.html')  

@app.route('/login', methods=['POST'])
def loginuser():
    users = mongo.db.user
    login_user = users.find_one({'email' : request.form['email']})
    print('login')
    if login_user is not None:
        if (request.form['password'] == login_user['password']):
            session['email'] = request.form['email']
            return render_template('home1.html')
    message="invalid username or password"        
    return render_template('login2.html' ,message=message)

@app.route('/signup', methods=['POST','GET'])
def register():
    
    if request.method == 'POST':
        users = mongo.db.user
        existing_user = users.find_one({'email' : request.form['email']})
        if existing_user is None:

            print('signup')
            users.insert_one({'firstname' : request.form['fname'],'lastname' : request.form['lname'],'phonenumber' : request.form['pnumber'] ,'email': request.form['email'] ,'password' : request.form['psw'],'confimpassword' : request.form['cpsw']})
            session['email'] = request.form['email']
            return render_template('home1.html')
        else:
            return 'That username already exists!'

    return render_template('signup1.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('login'))

@app.route('/crops')
def page1():
    return render_template('cropselection.html')

@app.route('/water')
def page2():
    return render_template('irrigation.html')

@app.route('/seed')
def page3():
    return render_template('seedingmethods.html')


@app.route('/protect')
def page4():
    return render_template('protection.html')    
      

@app.route('/vupload', methods=['POST','GET'])
def videoupload():
    
    if request.method == 'POST':
        users = mongo.db.contents
        users.insert_one({'title' : request.form['vtitle'],'description' : request.form['vdes'],'file' : request.files['file'].filename })
        f = request.files['file']
        os.chdir('video')
        f.save(f.filename)
        os.chdir('/..')
        return render_template('video.html')
        
        # return render_template('video.html')
    else:
       return render_template('vupload.html')
# file.save(os.path.join("/video/", filename))


@app.route('/vpage')
def videopage():
    videos=mongo.db.contents
    cursor = videos.find()
    all_data = list(cursor)
    video_names=os.listdir('E:/techagr/video')
    return render_template('video.html' , videolist=all_data, video_names=video_names)

@app.route('/static/video/<filename>')
def send_video(filename):
    return send_from_directory("video",filename)


@app.route('/croppage' ,methods=['GET', 'POST'])
def cropsearch():    
    if request.method == 'POST':
        crops = mongo.db.crop
        state=request.form.get('listBox')
        district=request.form.get('secondlist')
        district=district.upper()
        season=request.form.get('thirdlist')
        season=season.lower()
        season=season.capitalize()
        print(state)
        print(district.upper())
        print(season)
        some = {'State_Name' : state ,
                              'District_Name' : district.upper(),
                               'Season' : season  }
       
        crop1=crops.find({'State_Name' : state ,
                              'District_Name' : district.upper(),
                               'Season' : season  })
        print(crop1)
        for c in crop1:
            return render_template('cropsuggest2.html',c=c)
    else:
        print('yyyy')
        return render_template('cropsuggest1.html')




if __name__ == '__main__':
    app.run(debug=True)
