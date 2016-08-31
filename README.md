# App Store Reminder
## 简介
喜欢的app降价了？更新了？下架了又或者重新上架了？
脚本一键监听，邮件提醒，就这么点功能。
## 使用说明
* 修改config.ini配置邮箱
```json
  {
    "sender": "",						//请填入发件的邮箱号
    "password": "",					//请填入发件的邮箱密码
    "receiver": "",					//请填入收件的邮箱号
    "app_lost_mail": true,			//app下架上架推送开关
    "app_update_mail": true,			//app更新推送开关
    "app_cut_price_mail": true		//app降价推送开关
  }
```
* 运行search_app.py
  输入app的名称搜索app并加入监听列表

* 运行handler_app.py
  运行一次刷新一次监听列表中的app，发现变化邮件通知
  推荐先本地运行一次检测邮件连接情况，之后加入定时任务中指定频率刷新即可

## 注意事项
* 发件邮箱必须开始smtp服务
* 由于QQ邮箱升级，无法使用QQ密码登陆，需生成授权码。[详情戳这里](http://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256)
