from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_remove_comment_gid_remove_comment_mehmonxona_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="gid",
            name="bio",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="gid",
            name="experience_years",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="gid",
            name="instagram",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="gid",
            name="telegram",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
