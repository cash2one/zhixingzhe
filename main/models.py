from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User, related_name='profile')

    # 用户姓名
    name = models.CharField(null=True, blank=True, max_length=14)

    # 用户邮箱
    email = models.EmailField(null=True)

    # 用户描述信息
    desc = models.CharField(null=True, blank=True, max_length=30, default='这个用户很懒，还没有描述信息')

    # 用户头像
    avatar = models.ImageField(upload_to="avatars", default="avatars/default.jpg")

    def __str__(self):
        return self.name

class Topic(models.Model):
    # 话题名称
    name = models.CharField(null=True, blank=True, max_length=14)
    def __str__(self):
        return self.name

class Question(models.Model):
    # 问题提出者
    author = models.ForeignKey(to=User, related_name='question_author')

    # 问题标题
    title = models.CharField(max_length=100)

    # 问题描述
    desc = models.CharField(null=True, blank=True, max_length=1000)

    # 话题列表
    topic = models.ManyToManyField(Topic)

    # 回答数目
    answer_counts = models.IntegerField(default=0)

    # 问题创建时间
    createtime = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class Answer(models.Model):
    # 回答所属问题
    question =  models.ForeignKey(to=Question, related_name='question_answer')

    # 回答者
    author = models.ForeignKey(to=User, related_name='answer_author')

    # 回答内容
    content = RichTextUploadingField('回答')

    # 赞同数目
    like_counts = models.IntegerField(default=0)

    # 不赞同数目
    dislike_counts = models.IntegerField(default=0)

    # 评论数目
    comment_counts = models.IntegerField(default=0)

    # 回答创建时间
    createtime = models.DateField(auto_now=True)

    def __str__(self):
        return  self.question.title[:10]+":    "+str(self.author)+":    "+str(self.content)[:10]+":    "


class Comment(models.Model):
    # 评论者
    author = models.ForeignKey(to=User, related_name='comment_author')

    # 评论所属回答
    answer = models.ForeignKey(to=Answer, related_name='answer_comments')

    # 评论内容
    content = models.TextField(null=True, blank=True)

    # 评论时间
    createtime = models.DateField(auto_now=True)

    def __str__(self):
        return  self.content

class Vote(models.Model):

    VOTE_CHOICES = (
        ('like', 'like'),
        ('dislike', 'dislike'),
        ('normal', 'normal'),
        )

    voter = models.ForeignKey(to=User, related_name='vote_user')

    question = models.ForeignKey(to=Question, related_name='vote_question')

    answer = models.ForeignKey(to=Answer, related_name='vote_answer')

    ticket = models.CharField(choices=VOTE_CHOICES, max_length=10, default='normal')

    def __str__(self):
        return  self.voter.username+":    "+str(self.question.title)[:10]+":    "+str(self.answer)[:10]+":    "+str(self.ticket)


# for i in range(8):
#     username = 'puppy'+str(i+1)
#     email = username+"@muggle.com"
#     u=User(username=username,email=email)
#     u.set_password('muggle123456')
#     u.save()

# for i in range(8):
#     username = 'puppy'+str(i+1)
#     email = username+"@muggle.com"
#     u=User.objects.get(username=username)
#     p=UserProfile(belong_to=u)
#     p.email=email
#     p.save()
#
# for i in range(8):
#     username = 'puppy'+str(i+1)
#     name = 'pupy'+str(i+1)
#     email = username+"@muggle.com"
#     p=UserProfile.objects.get(email=email)
#     p.name=name
#     p.save()
