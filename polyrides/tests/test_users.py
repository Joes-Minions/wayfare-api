import requests
import unittest

_TEST_USERS = [
    {  # id: 1
        'first_name': 'Oliver',
        'last_name': 'Wang',
        'email': 'owang02@calpoly.edu',
        'password': 'password123'
    },
    {  # id: 2
        'first_name': 'Karissa',
        'last_name': 'Bennett',
        'email': 'kbenne09@calpoly.edu',
        'password': 'deadlifts'
    },
    {  # id: 3
        'first_name': 'Barack',
        'last_name': 'Obama',
        'email': 'test@example.com',
        'password': 'america'
    },
    {  # id: 4
        'first_name': 'Minh-Quan',
        'last_name': 'Tran',
        'email': 'mtran22@calpoly.edu',
        'password': 'Yeah, my password is really long.'
    }
]

class TestUsers(unittest.TestCase):
    def setUp(self):
        """Replace all source data with test user data."""
        scheme = 'http://'
        base_url = 'localhost'
        port = 5000
        route = 'users'
        self.endpoint = '{}{}:{}/{}'.format(scheme, base_url, port, route)
        # Clear source and load all test data.
        requests.delete(self.endpoint)
        for user in _TEST_USERS:
            requests.post(self.endpoint, user)

    def test_get_and_id_generation(self):
        response = requests.get(self.endpoint).json()
        self.assertEqual(len(response), 4)
        for index, user in enumerate(response):
            self.assertEqual(user['id'], index + 1)
            self.assertEqual(user['email'], _TEST_USERS[index]['email'])

    def test_post_missing_first_name(self):
        response = requests.post(self.endpoint, {
            'last_name': 'test',
            'email': 'test',
            'password': 'test'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), "Missing field: 'first_name'")

    def test_post_missing_last_name(self):
        response = requests.post(self.endpoint, {
            'first_name': 'test',
            'email': 'test',
            'password': 'test'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), "Missing field: 'last_name'")

    def test_post_missing_email(self):
        response = requests.post(self.endpoint, {
            'first_name': 'test',
            'last_name': 'test',
            'password': 'test'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), "Missing field: 'email'")

    def test_post_missing_password(self):
        response = requests.post(self.endpoint, {
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), "Missing field: 'password'")

    def test_post_duplicate_email(self):
        duplicate_email = _TEST_USERS[0]['email']
        response = requests.post(self.endpoint, {
            'first_name': 'test',
            'last_name': 'test',
            'email': duplicate_email,
            'password': 'test'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), "Duplicate email: '{}'".format(duplicate_email))

    def test_post(self):
        new_user = {
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test',
            'password': 'test'
        }
        post_response = requests.post(self.endpoint, new_user)
        self.assertEqual(post_response.status_code, 201)
        self.assertEqual(post_response.json(), '')
        new_user.update({
            'id': len(_TEST_USERS) + 1
        })
        get_response = requests.get(self.endpoint).json()[-1]
        self.assertEqual(get_response, new_user)


if __name__ == '__main__':
    unittest.main()
