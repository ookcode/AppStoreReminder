# App Store Reminder
[中文版本](https://github.com/ookcode/AppStoreReminder/blob/master/README_zh.md)
## Introduction
Did you want to get a notification when your favorite apps cut price,updated,or out off the shelf in the appstore?
This Script Help you to monitor these apps.

## Instructions for use
* edit config.ini
```javascript
  {
    "sender": "",   // please enter a sender e-mail address
    "password": "", // please enter a sender e-mail password
    "receiver": "", // please enter a receiver e-mail address
    "app_lost_mail": true,      // app avaible push switch
    "app_update_mail": true,    // app update push switch
    "app_cut_price_mail": true  // app price push switch
  }
```
* search_app.py
  `$python search_app.py`
  Enter the name of the app to search for the app and then add it to the listeners

* handler_app.py
  `$python handler_app.py`
  Each run will traverse the list of listeners and mail you the change.
  I recommended you join the script to the scheduler (linux crontab command) to make a frequency operation

## Precautions
* Sender E-mail must open smtp service