
from system.core.model import Model
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\.\_-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class User(Model):
    def __init__(self):
        super(User, self).__init__()


    def create_user(self, info):
        errors = []
        data = {
            'name' : info['name'],
            'alias' : info['alias'],
            'email' : info['email'],
            'password' : info['password'],
            'password_confirmation' : info['password_confirmation'],
            'birthday' : info['birthday']
                }
        if not data['name']:
            errors.append('Name must not be blank')
        elif len(data['name']) < 2:
            errors.append('Name must be at least 2 characters')
        elif not NAME_REGEX.match(data['name']):
            errors.append('Name field cannot contain numbers or special characters')
        if not data['alias']:
            errors.append('Alias must not be blank')
        elif len(data['alias']) < 2:
            errors.append('Your alias must be greater than 2 characters')
        if not data['email']:
            errors.append('Email must not be blank')
        elif not EMAIL_REGEX.match(data['email']):
            errors.append('Email format is incorrect')
        if not data['password']:
            errors.append('Password must not be blank')
        elif len(data['password']) < 8:
            errors.append('Password must be at least 8 characters')
        elif not data['password'] == data['password_confirmation']:
            errors.append('Your password confirmation does not match')
        if not data['birthday']:
            errors.append('Please enter your birthday')

        if errors:
            return {'status' : False, 'errors' : errors}

        data['pw_hash'] = self.bcrypt.generate_password_hash(data['password'])
        insert_user_query = 'INSERT INTO user (name, alias, email, pw_hash, birthday, created_at, updated_at) VALUES (:name, :alias, :email, :pw_hash, :birthday, NOW(), NOW());'
        insert_user = self.db.query_db(insert_user_query, data)

        user_id = {
            'id' : insert_user
        }
        select_new_user_query = 'SELECT * FROM user WHERE id= :id;'
        new_user = self.db.query_db(select_new_user_query, user_id)
        return {'status' : True, 'user' : new_user[0]}

    def login_user(self, info):
        errors = []
        data = {
            'email' : info['email'],
            'password' : info['password']
        }

        if not data['email']:
            errors.append('Email must not be blank')
        elif not EMAIL_REGEX.match(data['email']):
            errors.append('Email format is incorrect')
        if not data['password']:
            errors.append('Password must not be blank')

        if errors:
            return {'status' : False, 'errors' : errors}

        ### else if basic validation has passed :

        login_query = 'SELECT * FROM user WHERE email = :email LIMIT 1'

        user_login = self.db.query_db(login_query, data)

        if user_login:
            if self.bcrypt.check_password_hash(user_login[0]['pw_hash'], data['password']):
                return {'status' : True, 'user' : user_login[0]}

        errors.append('Email or password is incorrect')
        return {'status' : False, 'errors' : errors}
