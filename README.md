## What is x_note_autofill? ##

本程式為個人公司x_note系統 表單填取器

工作行程一般會在Google calendar 記戴, 而Note系統上每周也需要作相同的記錄。
為簡化流程編寫這一個簡單的程式，目前為0.1(20220530)的版本，可簡單運行。

本程式需要用戶在Google帳戶上開放API 並下戴credentials.json
可由 https://console.developers.google.com/ 進行產生相關授權

使用者可由 https://developers.google.com/calendar/api/quickstart/python 
來授權產生 token.json, 將credentials.json & token.json 和程式放在相同的
目錄之下就可以了。 

在Calendar的記錄中需在 日期中填寫備註，以便程式取用
* projectcode,L12XXXX,description,解析度問題處理,work,叫修服務/拆移機@

日歷的時間必須為整天

程式中
g_calendar.py : note_calendarId 必須(在你個人或其它日歷中，設定和共用 裡會有這個日歷專屬的ID)
webcapry_main.py : username, password 為servicenet登入的帳號/密碼


以上是0.1版的概述
