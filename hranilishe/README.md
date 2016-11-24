Пример использования:

    import hashlib

    from django.db import models
    from django.utils.translation import ugettext_lazy as _


    class ResourceModel(models.Model):
        filename = models.CharField(max_length=255, blank=True, null=True)
        resource = models.FileField(_(u'model'), max_length=256,
                                    upload_to=upload_by_hash, storage=HashedFileSystemStorage())
        size = models.PositiveIntegerField(default=0)
        is_compressed = models.BooleanField(default=False)
        is_deleted = models.BooleanField(default=False)

        # служебное поле, используется для организации хранения файлов,
        # см. функцию upload_by_hash выше
        md5sum = models.CharField(max_length=36)

        class Meta:
            abstract = True  # создаём поля в моделях-наследниках

        def fill_storage_metadata(self, user=None, session_key=None):
            u"""Вычисляет MD5 от содержимого файла и записывает его в поле модели.
            При сохранении функция upload_by_hash берёт вычисленный хэш из модели и
            записывает на файловую систему с помощью HashedFileSystemStorage.
            """
            if not self.pk:  # сохранение нового объекта
                md5 = hashlib.md5()
                for chunk in self.resource.chunks():
                    md5.update(chunk)
                self.md5sum = md5.hexdigest()
                self.size = self.resource.file.size
