# Generated by Django 4.0.3 on 2022-05-22 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('servicos', '0002_registro_user_alter_departamento_unidade_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro',
            name='status',
            field=models.CharField(choices=[('Pendente', 'Pendente'), ('Em andamento', 'Em andamento'), ('Finalizado', 'Finalizado'), ('Cancelado', 'Cancelado')], default='Pendente', max_length=15),
        ),
        migrations.AlterField(
            model_name='registro',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
    ]
