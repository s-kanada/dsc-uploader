"""
Modelにデータ取得を命令
プログラム的な処理はここに記載できる
戻り値はtemplatesへ
"""

import requests
from django.shortcuts import render
from uploader.forms import FileUploadForm
from datetime import datetime
import pytz

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

    if response.text and response.status_code == 200:
        data = response.json()
        folder_names = [item["name"] for item in data if item["type"] == "dir"]
        return folder_names
    else:
        return []

def subdir_list(selected_folder):
    url = GETLIST_URL
    json_data = {'dir_path': f"{DIR_PATH}{selected_folder}"}
    auth = (USERNAME, PASSWORD)

    response = requests.post(url, json=json_data, auth=auth)
    if response.text and response.status_code == 200:
        data = response.json()
        subfolder = [item["name"] for item in data if item["type"] == "dir" and item["name"] != "インポート済"]
        subfolder.insert(0, '--')
        return subfolder
    else:
        return ['--']

def upload_file(request):
    success_message = None
    error_message = None
    information = ""

    # 初回表示時に指定のキーをクリア
    if not request.session.get('initialized', False):
        request.session['initialized'] = True
        request.session.pop('file_history', None)

    # アップロード先フォルダを取得
    folder_names = dir_list()
    selected_folder = request.POST.get('folder_select')
    request.session['last_selected_folder'] = selected_folder

    # アップロード先サブフォルダを取得
    subfolders = subdir_list(selected_folder)
    selected_subfolder = request.POST.get('subfolder_select')
    if selected_subfolder != "--":
        request.session['last_selected_subfolder'] = selected_subfolder
        selected_folder = f"{selected_folder}/{selected_subfolder}"
    
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
                    
                    url = UPDFILE_URL
                    dest_dir = f"{DIR_PATH}{selected_folder}"
                    data = {'dest_dir': dest_dir, 'overwrite': 'true'}
                    auth = (USERNAME, PASSWORD)

                    # ファイルを 'file' パラメータに指定
                    files_data = {'file': (file.name, file)}

                    response = requests.post(url, data=data, auth=auth, files=files_data)

                    if response.status_code in (200, 201):
                        url = GETLIST_URL
                        json_data = {'dir_path': dest_dir}

                        response = requests.post(url, json=json_data, auth=auth)

                        if response.status_code == 200:
                            data = response.json()
                            matching = [record for record in data if record["name"] == file_name]
                            # matching_records の中から modified の値を取得
                            file_time = matching[0]["modified"]
                            # UTC時間の文字列をdatetimeオブジェクトに変換
                            utc_time = datetime.strptime(file_time, "%Y-%m-%dT%H:%M:%S.%fZ")

                            # UTCタイムゾーンを表すオブジェクトを取得
                            utc_timezone = pytz.timezone("UTC")

                            # 日本のタイムゾーンを表すオブジェクトを取得
                            japan_timezone = pytz.timezone("Asia/Tokyo")

                            # UTC時間を日本時間に変換
                            japan_time = utc_time.replace(tzinfo=utc_timezone).astimezone(japan_timezone)

                            # 日本時間の文字列に変換
                            japan_time_str = japan_time.strftime("%Y/%m/%d %H:%M:%S")

                        # API呼び出しが成功した場合の処理
                        success_message = f"ファイルのアップロードに成功しました。"
                    else:
                        # API呼び出しが失敗した場合の処理
                        error_message = f"ファイルのアップロードに失敗しました。({response.status_code} - {response.text})"

                    # ファイル情報をセッションに保存
                    if 'file_history' not in request.session:
                        request.session['file_history'] = []
                    request.session['file_history'].append({'file_name': file_name, 'success_message': success_message, 'error_message': error_message, 'file_time': japan_time_str})
            else:
                # フォームが無効な場合の処理
                information = "アップロードするファイルを選択してください！"
        else:
            pass
    else:
        pass

    return render(request, 'uploader/upload.html', {'form': form, 'dir_list': folder_names, 'subdir_list': subfolders, 'information': information})

