from flask_app.config.mysqlconnection import connectToMySQL
#might need other imports like flash other classes and regex

db = 'Your database name'

class Rename:
    def __init__(self, data):
        #follow database table fields plus any other attribute you want to create
        pass


    @classmethod
    def rename(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db).query_db(query)
        #Nice little head start
        #Rest of code here
        print(results)
        return "Something here"