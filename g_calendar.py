# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

####填寫你個人的Google日歷Id
note_calendarId = ''
note_maxResults = 100

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def events():
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        #### timeMin 及 timeMax 決定我們要讀取日歷上時間區間，我們的系統需書寫的區間為一周
        #### 因些定調以周日 18:00 - 20:00 之間執行為主

        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        sevendayago = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).isoformat() + 'Z'
        events_result = service.events().list(calendarId=note_calendarId, timeMin=sevendayago, timeMax=now,
                                              maxResults=note_maxResults, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return None
        else:
            return events

    except HttpError as error:
        print('An error occurred: %s' % error)


def get_cal_week_info_by_day(events):
    #### 因為我們需要在日歷的備註中抓取所需的資料，所以會檢查description的內容是否有值
    #### 會用時間中的日期為資料index，目前沒有處理日歷中非整日的多項時間處理，因此需每
    #### 日只有一筆工作項目及時間寫整日

    rows = {}
    for event in events:
        if 'description' in event:
            start = event['start'].get('dateTime', event['start'].get('date'))
            note_day = event['start'].get('date').split('-')[2]
            rows[note_day] = event['description']
    return rows

def get_one_row_data(rows, day):
    #### 取單筆的值來作Work SOP

    if day in rows:
        import re
        #預設取@符號前的字串，因此說明文字內不能有@
        input_string_list = re.sub(r"\@.*", "", rows[day]).split(',')
        return input_string_list
    else:
        return None

def get_current_date():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
