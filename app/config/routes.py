
from system.core.router import routes

routes['default_controller'] = 'Users'
routes['/'] = 'Users#index'
routes['POST']['/register'] = 'Users#register'
routes['POST']['/login'] = 'Users#login'

routes['/pokes'] = 'Users#pokes'
routes['POST']['/pokes/<int:id>'] = 'Users#poke_me'




routes['/logout'] = 'Users#logout'
