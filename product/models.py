from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class Product(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def distribute_users_to_groups(self):
        groups = self.group_set.annotate(num_users=Count('users')).order_by('num_users')

        for user in self.users.all():
            group = groups.first()

            if group.num_users >= group.max_users:
                # Если группа уже заполнена, создаем новую
                group = Group.objects.create(product=self, name='Group {}'.format(groups.count() + 1),
                                             min_users=self.min_users, max_users=self.max_users)

            group.users.add(user)
            group.save()

    def grant_access_to_user(self, user):
        # Проверяем, что текущая дата больше или равна дате начала продукта
        if timezone.now() >= self.start_date:
            self.users.add(user)
            self.distribute_users_to_groups()
        else:
            # Если продукт ещё не начался, можно пересобрать группы
            self.users.add(user)
            self.rearrange_groups()

    def rearrange_groups(self):
        # Удаляем всех пользователей из групп
        self.group_set.update(users=None)

        # Запускаем алгоритм распределения пользователей
        self.distribute_users_to_groups()

class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    video_link = models.CharField(max_length=200)

class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    min_users = models.PositiveIntegerField()
    max_users = models.PositiveIntegerField()
    users = models.ManyToManyField(User)