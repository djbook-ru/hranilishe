# -*- coding: utf-8 -*-

u"""Модуль реализует хранилище медиа файлов. Имя файла для хранения модели
генерируется с помощью хэш функции."""

import os

from django.core.files.storage import FileSystemStorage


class HashedFileSystemStorage(FileSystemStorage):
    u"""
    Реализация файлового хранилища для поля модели, которое использует
    хэши для имён сохраняемых в него файлов.
    """
    def get_available_name(self, name):
        u"""Тут можно влиять на генерацию имени файла в хранилище."""
        return name

    def _save(self, name, content):
        u"""Для перерисовки модели после изменения её поворота по осям,
        необходимо заменять отрендеренный файл в хранилище."""
        if self.exists(name):
            return name
        return super(HashedFileSystemStorage, self)._save(name, content)


def upload_by_hash(instance, filename):
    """Формируем путь для сохранения файлов."""
    h = instance.md5sum  # см. поле `md5sum` в модели
    basename, ext = os.path.splitext(filename)
    return os.path.join('storage', h[0:1], h[1:2], h + ext.lower())
