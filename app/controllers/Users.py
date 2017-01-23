
from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)

        self.load_model('User')
        self.load_model('Poke')


    def index(self):
        return self.load_view('index.html')

    def register(self):
        data = {
            'name' : request.form['name'],
            'alias' : request.form['alias'],
            'email' : request.form['email'],
            'password' : request.form['password'],
            'password_confirmation' : request.form['password2'],
            'birthday' : request.form['birthday']
                }

        user_create = self.models['User'].create_user(data)

        if user_create['status'] == False:
            if user_create['errors']:
                for error in user_create['errors']:
                    flash(error, 'error')
            return redirect('/')
        elif user_create['status'] == True:
            session['user'] = user_create['user']
            return redirect('/pokes')

    def login(self):
        data = {
            'email' : request.form['email'],
            'password' : request.form['password']
        }

        user_login = self.models['User'].login_user(data)

        if user_login['status'] == False:
            if user_login['errors']:
                for error in user_login['errors']:
                    flash(error, 'error2')
            return redirect('/')

        elif user_login['status'] == True:
            session['user'] = user_login['user']
            return redirect('/pokes')



    def pokes(self):
        if not 'user' in session: return redirect('/')

        data = {
            'session_id' : session['user']['id']
        }

        pokes = self.models['Poke'].show_all_pokes(data)

        who_poke_me = self.models['Poke'].who_poke_me(data)

        how_many_count = len(who_poke_me)

        return self.load_view('pokes.html', user=session['user'], pokes = pokes, who_poke_me = who_poke_me, how_many_count = how_many_count)

    def poke_me(self, id):
        data = {
            'user_id' : session['user']['id'],
            'friend_id' : id
        }
        poke_id = self.models['Poke'].poke_me(data)
        return redirect('/pokes')


    def logout(self):
        session.clear()

        return redirect('/')
