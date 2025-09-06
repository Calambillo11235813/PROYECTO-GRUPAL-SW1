from django.db import migrations, models
import django.utils.timezone
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('texto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='analisistexto',
            name='tipo_entrada',
            field=models.CharField(
                choices=[('TEXTO', 'Texto directo'), ('ARCHIVO', 'Archivo subido')],
                default='TEXTO',
                max_length=10
            ),
        ),
        migrations.AddField(
            model_name='analisistexto',
            name='nombre_archivo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='analisistexto',
            name='tamano_archivo',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='analisistexto',
            name='tipo_archivo',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.CreateModel(
            name='ArchivoAnalisis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ruta_archivo_original', models.CharField(blank=True, max_length=500, null=True)),
                ('hash_archivo', models.CharField(blank=True, max_length=64, null=True)),
                ('fecha_subida', models.DateTimeField(default=django.utils.timezone.now)),
                ('analisis', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='archivo_info', to='texto.analisistexto')),
            ],
            options={
                'verbose_name': 'Archivo de Análisis',
                'verbose_name_plural': 'Archivos de Análisis',
                'db_table': 'archivo_analisis',
            },
        ),
    ]