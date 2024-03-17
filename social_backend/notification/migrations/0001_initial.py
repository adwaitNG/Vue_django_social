# Generated by Django 5.0.2 on 2024-03-17 23:10

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0011_trends'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('body', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('type_of_notification', models.CharField(choices=[('newFriendRequest', 'New friendrequest'), ('acceptedFriendRequest', 'Accepted friendrequest'), ('rejectedFriendRequest', 'Rejected friendrequest'), ('postLike', 'Post like'), ('postComment', 'Post comment')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_notification', to=settings.AUTH_USER_MODEL)),
                ('created_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recived_notification', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='post.post')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
    ]
