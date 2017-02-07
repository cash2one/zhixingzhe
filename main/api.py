from django.contrib.auth.models import User
from blog.models import UserProfile, Answer,  Question, Vote, Topic, Vote, Comment
from django.contrib.auth.decorators import login_required
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model =Topic
        fields = ('name',)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =UserProfile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile=UserProfileSerializer()
    class Meta:
        model =User
        fields = ('id','username','profile')

class CommentSerializer(serializers.ModelSerializer):
    author=UserSerializer()
    class Meta:
        model =Comment
        fields = ('author', 'content', 'createtime')
        depth=1

class VorteSerializer(serializers.ModelSerializer):
    voter=UserSerializer()
    class Meta:
        model =Vote
        fields = ('voter', 'question', 'answer', 'ticket')

class AnswerSerializer(serializers.ModelSerializer):
    author=UserSerializer()
    answer_comments=CommentSerializer(many=True)
    class Meta:
        model = Answer
        fields =fields =('id', 'question', 'content', 'like_counts', 'dislike_counts', 'comment_counts','createtime', 'author', 'answer_comments')
        depth=1

class QuestionSerializer(serializers.ModelSerializer):
    question_answer = AnswerSerializer(many=True)
    vote_question=VorteSerializer(many=True)
    author=UserSerializer()
    topic=TopicSerializer(many=True)
    class Meta:
        model = Question
        fields =('id', 'author', 'title', 'desc', 'topic', 'answer_counts', 'createtime', 'question_answer','vote_question')
        depth=1

class GetProfileSerializer(serializers.ModelSerializer):
    profile=UserProfileSerializer()
    question_author=QuestionSerializer()
    answer_author=AnswerSerializer()
    class Meta:
        model =User
        fields = ('id','username','profile','question_author', 'answer_author')


@api_view(['GET', 'POST'])
# @authentication_classes((TokenAuthentication,))
def answers(request,start,end):
    answers = Answer.objects.all().order_by('-id')[int(start):int(end)+1]
    if request.method == 'GET':
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
# @authentication_classes((TokenAuthentication,))
def question_all(request):
    questions = Question.objects.all().order_by('-createtime')
    if request.method == 'GET':
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
# @authentication_classes((TokenAuthentication,))
def questions(request,id):
    questions = Question.objects.get(id=id)
    if request.method == 'GET':
        serializer = QuestionSerializer(questions)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
# @authentication_classes((TokenAuthentication,))
def topics(request):
    topics = Topic.objects.all()
    if request.method == 'GET':
        serializer = TopicSerializer(topics,many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
# @authentication_classes((TokenAuthentication,))
def getprofile(request,id):
    profile = User.objects.get(id=id)
    if request.method == 'GET':
        serializer = GetProfileSerializer(profile)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def question(request):
    try:
        user=User.objects.get(id=request.data['user_id'])
        title=request.data['title']
        desc=request.data['desc']
        q=Question(author=user,title=title,desc=desc)
        q.save()
        topics=request.data['topic'].split(' ')
        print (topics)
        for topic in topics:
            if topic:
                try:
                    t = Topic.objects.get(name=topic)
                except Exception as e:
                    t = Topic(name=topic)
                    t.save()
                    q.topic.add(t)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print("error:")
        print (e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
# @authentication_classes((TokenAuthentication,))
def push_comment(request):
    try:
        user=User.objects.get(id=int(request.data['user']))
        content=request.data['comment']
        answer=Answer.objects.get(id=int(request.data['answer_id']))
        c=Comment(author=user,content=content,answer=answer)
        c.save()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# @login_required(redirect_field_name='login')
# @authentication_classes((TokenAuthentication,))
@api_view(['POST'])
def push_answer(request):
    content = request.POST.get("content")
    question_id=request.POST.get("question_id")
    user=User.objects.get(id=request.POST.get('user_id'))
    question=Question.objects.get(id=request.POST.get("question_id"))
    try:
        try :
            count=Answer.objects.filter(question=question,author=user).count()
            if count>0:
                return Response({'msg':'you have ansered before'},status=status.HTTP_403_FORBIDDEN)
            else:
                raise Exception("there is no answer")
        except:
            answer = Answer(question=question, author=user)
            answer.content = content
            answer.save()
            question.answer_counts += 1
            question.save()
            return Response(status=status.HTTP_200_OK)
    except:
        return Response({'msg':'something wrong'},status=status.HTTP_403_FORBIDDEN)



# @login_required(redirect_field_name='login')
# @authentication_classes((TokenAuthentication,))
@api_view(['POST'])
def vote(request):
    user=User.objects.get(id=request.POST.get('user_id'))
    question_id = int(request.POST.get('question_id'))
    answer_id = int(request.POST.get('answer_id'))
    user_vote = request.POST['vote']
    answer=Answer.objects.get(id=answer_id,question_id=question_id)
    try:
        vote = Vote.objects.get(voter=user, question_id=question_id, answer_id=answer_id)
    except:
        vote = Vote.objects.create(voter=user, question_id=question_id, answer_id=answer_id)
    try:
        if user_vote == vote.ticket:
            if user_vote == 'like':
                vote.ticket='normal'
                answer.like_counts-=1
            if user_vote == 'dislike' :
                vote.ticket='normal'
                answer.dislike_counts-=1
        else:
            if user_vote == 'like':
                if vote.ticket == 'dislike':
                    answer.dislike_counts-=1
                vote.ticket = user_vote
                answer.like_counts+=1
            elif user_vote == 'dislike' :
                if vote.ticket == 'like':
                    answer.like_counts-=1
                vote.ticket = user_vote
                answer.dislike_counts+=1
        vote.save()
        answer.save()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response({'msg':'something wrong'},status=status.HTTP_403_FORBIDDEN)
