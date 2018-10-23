# Generated by Django 2.1.1 on 2018-10-19 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('df_user', '0002_auto_20181016_2027'),
        ('df_goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('count', models.IntegerField()),
                ('goods', models.ForeignKey(on_delete=None, to='df_goods.GoodsInfo')),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('oid', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('odate', models.DateTimeField(auto_now=True)),
                ('oIsPay', models.BooleanField(default=False)),
                ('ototal', models.DecimalField(decimal_places=2, max_digits=8)),
                ('oaddress', models.CharField(max_length=150)),
                ('user', models.ForeignKey(on_delete=None, to='df_user.UserInfo')),
            ],
        ),
        migrations.AddField(
            model_name='detailinfo',
            name='order',
            field=models.ForeignKey(on_delete=None, to='df_order.OrderInfo'),
        ),
    ]
