"""
viewからデータ取得の命令を受ける
データベースへアクセス
データベースから取得したデータをviewに返す
"""

from django.db import models

class FileUpload(models.Model):
    upload = models.FileField(upload_to='file/%Y/%m/%d')

