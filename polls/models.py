from django.db import models
import json

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    user = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    voted_user = models.CharField(max_length=200, default="[]")

    def __str__(self):
        return self.choice_text
    
    def set_voted_user(self, user):
        userList = json.loads(self.voted_user)
        userList.append(user)
        self.voted_user = json.dumps(userList)

    def get_voted_users(self):
        return json.loads(self.voted_user)
    
    def remove_voted_user(self, user):
        userList = json.loads(self.voted_user)
        userList.remove(user)
        self.voted_user = json.dumps(userList)
        self.votes -= 1
    
    def getID(self):
        return self.id