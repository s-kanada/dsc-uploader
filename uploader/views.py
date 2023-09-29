import requests
from django.shortcuts import render, redirect
from .forms import FileUploadForm

GETLIST_URL = "https://dsc0006sjp.drsum.com/api/v1.0/file/list"
UPDFILE_URL = "https://dsc0006sjp.drsum.com/api/v1.0/file/upload"
USERNAME = "u_rpa"
PASSWORD = "Cncgp135"
DIR_PATH = "D:/Shared/files/"
MAX_TIMEOUT = 900


def upload_file(request):
    success_message = None
    error_message = None

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # アップロードされたファイルを取得
            file = request.FILES['file']

            url = UPDFILE_URL
            dest_dir = f"{DIR_PATH}テスト"
            data = {'dest_dir': dest_dir, 'overwrite': 'true'}
            auth = (USERNAME, PASSWORD)

            # ファイルを 'file' パラメータに指定
            files_data = {'file': (file.name, file)}

            response = requests.post(url, data=data, auth=auth, files=files_data)

            if response.status_code in (200, 201):
                # API呼び出しが成功した場合の処理
                success_message = "ファイルのアップロードに成功しました。"
            else:
                # API呼び出しが失敗した場合の処理
                error_message = f"ファイルのアップロードに失敗しました。({response.status_code} - {response.text})"
    else:
        form = FileUploadForm()

    return render(request, 'uploader/upload.html', {'form': form, 'success_message': success_message, 'error_message': error_message})

