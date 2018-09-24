from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.

# User 扩展字段
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    nickname = models.CharField(max_length=32, verbose_name='Nickname', default="")
    description = models.CharField(max_length=150, verbose_name='Description', default="")

    class Meta:
        verbose_name = 'nickname'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()


post_save.connect(create_user_profile, sender=User)


class Wlibrary(models.Model):
    name = models.CharField(max_length=500, verbose_name='TheoremName')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exp = models.TextField(verbose_name='explain')
    mcdc_1 = models.CharField(max_length=64, verbose_name='mcdc_1')
    mcdc_2 = models.CharField(max_length=64, verbose_name='mcdc_2')
    ref = models.CharField(max_length=500, verbose_name="Reference", default="")
    publish = models.DateTimeField(default=datetime.now, verbose_name='Time')

    class Meta:
        verbose_name = 'Wlibrary'
        verbose_name_plural = 'Wlibrary'

    def __str__(self):
        return self.name


class Nexus(models.Model):
    r_name = models.CharField(max_length=200, verbose_name='Nexu_name')

    class Meta:
        verbose_name = 'Nexu'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.r_name


class Relation(models.Model):
    t1 = models.ForeignKey(Wlibrary, on_delete=models.CASCADE, related_name='t1', verbose_name='t1_name')
    ref = models.CharField(max_length=500, verbose_name='Reference', default="")
    l_name_exp = models.CharField(max_length=500, verbose_name='Description')
    l_name_r = models.ForeignKey(Nexus, on_delete=models.CASCADE, verbose_name='R_name')
    t2 = models.ForeignKey(Wlibrary, on_delete=models.CASCADE, related_name='t2', verbose_name='t2_name')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 't1_name'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.t1.name


class Relation2(models.Model):
    t11 = models.IntegerField(verbose_name='relationship_t11')
    operator1 = models.CharField(max_length=54, default='')
    t12 = models.IntegerField(verbose_name='relationship_t12')
    exp = models.CharField(max_length=500, verbose_name='Description')
    relationship = models.ForeignKey(Nexus, on_delete=models.CASCADE, verbose_name='R_name')
    t21 = models.IntegerField(verbose_name='relationship_t21')
    operator2 = models.CharField(max_length=54, default='')
    t22 = models.IntegerField(verbose_name='relationship_t22')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    ref = models.CharField(max_length=500, verbose_name='Reference', default="")

    class Meta:
        verbose_name = 'relationship_operator'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.exp


class Comment(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=20, default='佚名')
    content = models.CharField(verbose_name="内容", max_length=300)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    wlibrary = models.ForeignKey(Wlibrary, verbose_name="定理", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "博客评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content[:10]


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")

    send_type = models.CharField(verbose_name=u"验证码类型", max_length=10,
                                 choices=(("register", u"注册"), ("forget", u"找回密码")))
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)


class Operator(models.Model):
    type = models.CharField(max_length=64, verbose_name='type')

    class Meta:
        verbose_name = 'Operator'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type
