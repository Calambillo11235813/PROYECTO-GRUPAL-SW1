from django.db import models

<<<<<<< HEAD
class CodigoUpload(models.Model):
    file = models.FileField(upload_to='codigo/')
    filename = models.CharField(max_length=255)
    ast_json = models.TextField(null=True, blank=True)
    complejidad = models.FloatField(default=0)
    predict_score = models.FloatField(default=0)

    # 🔹 NUEVOS CAMPOS
    naming_score = models.FloatField(null=True, blank=True)
    repetitividad = models.FloatField(null=True, blank=True)
    tipo_codigo = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename
=======
# Create your models here.
>>>>>>> UNION
