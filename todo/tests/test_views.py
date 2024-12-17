from authentication.models import User
from utils.testSetp import TestSetup
from django.urls import reverse
from todo.models import Todo




class testModel(TestSetup):
    def test_should_create_todo(self):
        user = self.create_test_user()
        self.client.post(reverse('login'))
        updated_todos = Todo.objects.all()
        self.assertEqual(updated_todos.count(),1)
        response = self.client.post(reverse('createTodo'),{
                                      'owner':user,
                                       'title':'hello just do it',
                                       'description':'remember to do it'
                    })
        
        self.assertEqual(response.status_code, 302)