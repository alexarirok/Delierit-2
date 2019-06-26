import unittest, os, json
from app import create_app, db

class ParcelTestCase(unittest.TestCase):
    #This represent Delierit test case

    def setUp(self):
        #define test variables and initialize app.
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.parcel = {'name': 'Order for water tank Nyali'}
        # binds the app to the current context

        with self.app.app_context():
            # create all tables
            db.drop_all()
            db.session.close()
            db.create_all()

    def register_user(self, email="user@test.com", password="test1234"):
        #This helper method helps register a test user.
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/register', data=user_data)

    def login_user(self, email="user@test.com", password="test1234"):
        # This helper method helps log in a test user
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=user_data)
    
    def test_parcel_creation(self):
        #Test API can create a parcels (POST request)
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # create a bucketlist by making a POST request
        res = self.client().post(
            '/parcels/', 
            headers=dict(Authorization="Bearer " + access_token),
            data = self.parcel)
        self.assertEqual(res.status_code, 201)

        # get all the parcels that belong to test user by making a get request
        res = self.client().get(
            '/parcels/',
            headers=dict(Authorization="Bearer" + access_token),
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn('', str(res.data))

    def test_api_can_get_all_parcels(self):
        #test API can get a parcels (GET request)
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        #create a parcel by making a POST request
        res = self.client().post(
            '/parcels/', 
            headers=dict(Authorization="Bearer" + access_token),
            data=self.parcel)
        self.assertEqual(res.status_code, 201)

        #get all the parcelsthat belong to the test user by making a get request
        res = self.client().get(
            '/parcels/',
            headers=dict(Authorization="Bearer" + access_token)
        )
       
        self.assertEqual(res.status_code, 201)
        self.assertIn('', str(res.data))

    def test_api_can_get_parcel_by_id(self):
        #test API can get a single parcel using its id
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post(
            '/parcels/',
            headers=dict(Authorization="Bearer" + access_token), 
            data=self.parcel)

        # assert that the parcel is created    
        self.assertEqual(rv.status_code, 201)
        # get the response data in json format
        results = json.loads(rv.data.decode())

        result = self.client().get(
            '/parcels/{}'.format(results['id']),
            headers=dict(Authorization="Bearer" + access_token))

            # assert that the parcel is actually returned
        self.assertEqual(result.status_code, 200)
        self.assertIn('', str(result.data))

    def test_parcel_can_be_edited(self):
        #Test API can edit an existing parcel. (PUT request)
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        
        # first, we create a parcel by making a POST request
        rv = self.client().post(
            '/parcels/',
             headers=dict(Authorization="Bearer " + access_token),
            data={'name':'order, buy, and sell'})
        self.assertEqual(rv.status_code, 201)

        # get the json with the parcel
        results = json.loads(rv.data.decode())

        # then , we edit the created parcel by making a PUT request
        rv = self.client().put(
            '/parcels/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data={
                "name": "Dont just order, but also buy and sell :-)"
            })
        self.assertEqual(rv.status_code, 200)

        #finally we get the edited parcel to see if it is actualy edited 
        results = self.client().get(
            '/parcels/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token)
        self.assertIn('', str(results.data))

    def test_parcel_deletion(self):
        #Test API can delete an existing parcel. (DELETE request)
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post(
            '/parcels/',
            headers=dict(Authorization="Bearer " + access_token),

            data={'name': 'order, buy and sell'})
        self.assertEqual(rv.status_code, 201)
        # get the parcel in json
        results = json.loads(rv.data.decode())
        # delete the parcel we just created

        res = self.client().delete(
            '/parcels/{}'.format(results['id']),
            headers=dict(Authorization="Bearer" + access_token)),
        self.assertEqual(res.status_code, 200)
     
        #Test to see if it exists, should return a 404
        result = self.client().get(
            '/parcels/1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)

    # def tearDown(self):
    #     #teardown all initialized variables.
    #     with self.app.app_context():
    #         #drdrop all tables
    #         db.session.remove()
    #         db.drop_all()

# make the tests conviniently executable
if __name__ == '__main__':
    unittest.main()
        