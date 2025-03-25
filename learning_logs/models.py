from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    """用户学习的主题"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        """返回模型的字符串表示"""
        return self.text
    
class Entry(models.Model):
    """学习到的有关某个主题的具体知识"""
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE) #让Django在删除主题的同时删除所有与之相关联的条目，这称为级联删除(cascadingdelete)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    # 在Entry类中嵌套了Meta类,它让我们能够设置一个特殊属性，让Django在需要时使用Entries来表示多个条目
    class Meta:
        verbose_name_plural = 'entries' 

    def __str__(self):
        """返回模型的字符串表示"""
        return f"{self.text[:50]}..."
