"""
Modelにデータ取得を命令
プログラム的な処理はここに記載できる
戻り値はtemplatesへ
"""

import requests
from django.shortcuts import render
from uploader.forms import FileUploadForm


GETLIST_URL = "https://dsc0006sjp.drsum.com/api/v1.0/file/list"
UPDFILE_URL = "https://dsc0006sjp.drsum.com/api/v1.0/file/upload"
USERNAME = "u_rpa"
PASSWORD = "Cncgp135"
DIR_PATH = "D:/Shared/files/"
MAX_TIMEOUT = 900

def dir_list():
    url = GETLIST_URL
    json_data = {'dir_path': DIR_PATH}
    auth = (USERNAME, PASSWORD)

    response = requests.post(url, json=json_data, auth=auth)

    if response.status_code == 200:
        data = response.json()
        folder_names = [item["name"] for item in data if item["type"] == "dir"]
        return folder_names
    else:
        return []

def upload_file(request):
    success_message = None
    error_message = None
    information = ""
    # アップロード先フォルダを取得
    folder_names = dir_list()
    selected_folder = request.POST.get('folder_select')
    request.session['last_selected_folder'] = selected_folder
    
    form = FileUploadForm()

    if request.method == 'POST':
        if 'action' in request.POST and request.POST['action'] == 'clear':
            if 'file_history' in request.session:
                del request.session['file_history']
            form.is_valid = lambda: True

        elif 'action' in request.POST and request.POST['action'] == 'upload':
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                # アップロードされたファイルを取得
                uploaded_files = request.FILES.getlist('file')

                for file in uploaded_files:
                    file_name = file.name
                    # ファイル情報をセッションに保存
                    if 'file_history' not in request.session:
                        request.session['file_history'] = []
                    request.session['file_history'].append({'file_name': file_name})
                    
                    url = UPDFILE_URL
                    dest_dir = f"{DIR_PATH}{selected_folder}"
                    data = {'dest_dir': dest_dir, 'overwrite': 'true'}
                    auth = (USERNAME, PASSWORD)

                    # ファイルを 'file' パラメータに指定
                    files_data = {'file': (file.name, file)}

                    response = requests.post(url, data=data, auth=auth, files=files_data)

                    if response.status_code in (200, 201):
                        # API呼び出しが成功した場合の処理
                        success_message = f"ファイルのアップロードに成功しました。（アップロード先：{selected_folder}）"
                    else:
                        # API呼び出しが失敗した場合の処理
                        error_message = f"ファイルのアップロードに失敗しました。({response.status_code} - {response.text})"
            else:
                # フォームが無効な場合の処理
                information = "アップロードするファイルを選択してください！"
        else:
            pass
    else:
        pass

    return render(request, 'uploader/upload.html', {'form': form, 'success_message': success_message, 'error_message': error_message, 'dir_list': folder_names, 'information': information})

