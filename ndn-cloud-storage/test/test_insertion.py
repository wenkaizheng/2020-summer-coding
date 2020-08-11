import os
import time
import sys
import pickle
import subprocess
from threading import Lock
#from watchdog.observers import Observer
#from watchdog.events import *
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from watcher import FileEventHandler
from watchdog.observers import Observer
SCOPES = ['https://www.googleapis.com/auth/drive']


def insertion():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credapi.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # find the folder zmj's id and upload 
    g = u'gdrive --access-token ' + creds.token + u' list'
    process = subprocess.Popen(g, shell=True, stdout=subprocess.PIPE)
    output, err = process.communicate()
    output_list = output.split('\n')[1:-1]
    items = []
    for file_info in output_list:
        file_id = file_info.split()[0]
       # file_id = file_id.encode("utf-8")
        g = u'gdrive --access-token '+creds.token + u' info ' + file_id
        process = subprocess.Popen(g, shell=True, stdout=subprocess.PIPE)
        output, err = process.communicate()
        items.append(output)
    parent_id = None
    for item in items:
            item = item.split('\n')[:-1]
            file_id = item[0][item[0].find(':')+2:]
            name = item[1][item[1].find(':')+2:]
            mime_type = item[3][item[3].find(':')+2:]
           # print(name,time,parent,file_id,mime_type,file_id)
            if mime_type == 'application/vnd.google-apps.folder' and name == 'zmj':
               parent_id = file_id
               break
    
    
    
    g = u'gdrive --access-token ' + creds.token + \
        u' upload --parent '+ parent_id + u' game1.flv'
    process = subprocess.Popen(g, shell=True, stdout=subprocess.PIPE)
    output, err = process.communicate()
    # print(output)
    print("30th")
    # os.remove('game1.flv')


def wait():
    mutex = Lock()
    prefix = 'game1'
    if os.path.exists('/zmj'):
        nums = ['./zmj/game1', './zmj/game1.html', './zmj/game1.flv.incomplete', './zmj/' + prefix+'_h264_1080p.mp4', './zmj/'+prefix +
            '_h264_240p.mp4', './zmj/'+prefix+'_h264_360p.mp4', './zmj/'+prefix+'_h264_480p.mp4', './zmj/'+prefix+'_h264_720p.mp4']
    else:
        nums = ['./zmj/game1', './zmj/game1.html', './zmj/game1.flv.incomplete', './zmj/' + prefix+'_h264_1080p.mp4', './zmj/'+prefix +
            '_h264_240p.mp4', './zmj/'+prefix+'_h264_360p.mp4', './zmj/'+prefix+'_h264_480p.mp4', './zmj/'+prefix+'_h264_720p.mp4', './zmj']
    observer = Observer()
    event_handler = FileEventHandler(nums, mutex, 'insert')
    observer.schedule(event_handler, '.', True)
    observer.start()
    break_condition = False
    while True:
        time.sleep(3)
        mutex.acquire()
        if len(nums) == 0:
            observer.stop()
            break_condition = True
        print(nums)
        mutex.release()
        if break_condition:
            break
    print('end')
    process.kill()
    sys.exit(0)


pwd = os.path.abspath('../') + '/'+'ndn_script.py -v info'
print(pwd)
insertion()
#t1 = threading.Thread(target=wait, args=())
# t1.start()
cmd = 'python '+pwd
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
wait()
