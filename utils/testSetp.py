from authentication.models import User
from django.test import TestCase
from faker import Faker

class TestSetup(TestCase):
    def setUp(self):

        self.faker= Faker()
        self.password= self.faker.paragraph(nb_sentences=5)

        print(self.faker.name().split(" ")[0])


        
        self.user = {
                 'username':self.faker.name().split()[0],
                 'email':self.faker.email(),
                 'password':self.password,
                 'password2':self.password
            }
        

    def create_test_user(self):
        user=User.objects.create_user(username='username',
            email='email@app.com')
        user.set_password('password12')

        return user
    
    def create_test_user_two(self):
        user=User.objects.create_user(username='username2',
            email='email@app.com')
        user.set_password('password2')

        return user

    def tearDown(self):
        
        return super().tearDown()    