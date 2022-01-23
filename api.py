from flask import Flask 
from flask_restful import Resource, Api, reqparse 
import pandas as pd
import ast

from pandas.io.parsers import read_csv 

app = Flask(__name__)
api = Api(app)

# /users
users_path = '../artifacts/users.csv' 
# /locations 

class Users(Resource):
    # Create CRUD methods for API Resource class
    def get(self):
        '''Reads 'database' (csv currently) and converts dataframe to dictionary
            It then passes the dictionary in JSON response along with error code'''
        data = pd.read_csv(users_path)
        data = data.to_dict()
        return ({'data': data}, 200)
        
    def post(self):
        '''Passes '''
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True, type=str)
        parser.add_argument('name', required=True)
        parser.add_argument('city', required=True)
        args = parser.parse_args()
        data = pd.read_csv(users_path)
        userId_list = data['userId'].tolist()
        
        if args['userId'] in userId_list:   
            return ({
                'message': f"{args['userId']} already exists" 
            }, 409)
        else: 
            data = data.append({
                'userId': args['userId'],
                'name': args['name'],
                'city': args['city'],
                'locations': []  
            }, ignore_index=True)
            data.to_csv(users_path, index=False)
            return ({'data': data.to_dict()}, 200)
        
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True, type=str) 
        args = parser.parse_args()
        
        data = pd.read_csv(users_path)
        userId_list = data['userId'].tolist()
        
        if args['userId'] in userId_list:
            data = data[data['userId'] != str(args['userId'])]
            data.to_csv(users_path, index=False)
            return( {'message': 'Delete successful'}, 200)
        else: 
            return({'message': f"{args['userId']} not found!"}, 404)
            
    
      
class Locations(Resource):
    pass
 
api.add_resource(Users, '/users')
api.add_resource(Locations, '/locations')


if __name__ == "__main__":
    app.run(debug=True)