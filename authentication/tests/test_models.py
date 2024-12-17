from authentication.models import User
from utils.testSetp import TestSetup




class testModel(TestSetup):
    def test_should_create_user(self):
        user = self.create_test_user()
        self.assertEqual(str(user),user.email)