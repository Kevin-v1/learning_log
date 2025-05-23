from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic,Entry
from .forms import TopicForm,EntryForm

# Create your views here.
def index(request):
    """学习笔记的主页"""
    return render(request,'learning_logs/index.html')  #函数render()提供了两个实参：对象request以及一个可用于创建页面的模板

@login_required
def topics(request):
    """显示所有主题"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')  #查询数据库——请求提供Topic对象，并根据属性date_added进行排序。返回的查询集被存储在topics中
    context = {'topics':topics}  #定义一个将发送给模板的上下文。上下文是一个字典，其中的键是将在模板中用来访问数据的名称，而值是要发送给模板的数据
    return render(request,'learning_logs/topics.html',context)

@login_required
def topic(request,topic_id):
    """显示单个主题及其所有的条目"""
    topic = Topic.objects.get(id=topic_id)
    # 确认请求的主题属于当前的用户
    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by('-date_added') #获取与该主题相关联的条目
    context = {'topic':topic,'entries':entries} 
    return render(request,'learning_logs/topic.html',context)

@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据：创建一个表单
        form = TopicForm()
    else:
        # POST提交的数据：对数据进行处理
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
        
    # 显示空表单或指出表单数据无效
    context = {'form':form}
    return render(request,'learning_logs/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    """在特定主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = EntryForm()
    else:
        # POST提交的数据：对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # 先把表单里的数据转换成一个对象，但“先不要保存到数据库”，我还要手动补充一些字段（比如关联的 topic），再保存。
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic',topic_id = topic_id)
        
    # 显示空白表单或指出表单数据无效
    context = {'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
    """编辑既有条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # 初次请求使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据：对数据进行处理
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic',topic_id=topic.id)
        
    context = {'entry':entry,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_entry.html',context)