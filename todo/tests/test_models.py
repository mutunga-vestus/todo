from authentication.models import User
from utils.testSetp import TestSetup

from todo.models import Todo




class testModel(TestSetup):
    def test_should_create_user(self):
        user = self.create_test_user()
        

        todo=Todo(owner=user,title='coding',description='do it')
        todo.save

        self.assertEqual(str(todo),'coding')