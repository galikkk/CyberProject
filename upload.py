from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

upload_file_list = [r'C:\Users\galik\PycharmProjects\cyber_project\2022-04-01 08.42.22.985825.mp4']
for upload_file in upload_file_list:
    gfile = drive.CreateFile({'parents': [{'id': '1fvB8jlZ855MHywhuZOkSjIsehEcFMyFQ'}]})
    # Read file and set it as the content of this instance.
    gfile.SetContentFile(upload_file)
    gfile.Upload()  # Upload the file.

file_list = drive.ListFile(
    {'q': "'{}' in parents and trashed=false".format('1fvB8jlZ855MHywhuZOkSjIsehEcFMyFQ')}).GetList()
for file in file_list:
    print('title: %s, id: %s' % (file['title'], file['id']))


