
from system.core.model import Model

class Poke(Model):
    def __init__(self):
        super(Poke, self).__init__()

    def show_all_pokes(self, info):
        data = {
            'session_id' : info['session_id']
        }
        show_all_query = 'SELECT user.id AS id, user.name AS name, user.alias AS alias, user.email AS email, COUNT(poke.friend_id) AS poke_history FROM user LEFT JOIN poke ON user.id=poke.friend_id WHERE user.id <> :session_id GROUP BY user.id;'
        ### phew

        pokes =  self.db.query_db(show_all_query, data)

        return pokes

    def poke_me(self, info):
        data = {
            'user_id' : info['user_id'],
            'friend_id' : info['friend_id']
        }

        poke_query = 'INSERT INTO poke (user_id, friend_id, created_at, updated_at) VALUES (:user_id, :friend_id, NOW(), NOW());'

        poke_id = self.db.query_db(poke_query, data)
        return poke_id


    def who_poke_me(self, info):
        data = {
            'user_id' : info['session_id']
        }

        who_poke_me_query = 'SELECT poker.name AS friend, pokee.name AS me, COUNT(poke.friend_id) AS poked_me FROM poke LEFT JOIN user AS poker ON poker.id=poke.user_id LEFT JOIN user AS pokee ON poke.friend_id = pokee.id WHERE pokee.id=:user_id GROUP BY poker.id ORDER BY poked_me DESC;'
        ### phew

        who_poke_me = self.db.query_db(who_poke_me_query, data)

        return who_poke_me
