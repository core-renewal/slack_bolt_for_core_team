# slack_bolt_for_core_team
.envファイルとUserList.pyはgitignoreしているのでローカルで準備する
### 環境変数
.envファイルに`SLACK_BOT_TOKEN`と`SLACK_APP_TOKEN`と`TARGET_CHANNEL_ID`を設定する
### UserList
UserList.pyの中に
```
{
    "git user name":"slack user id",
    ...
}
```
の形式でリストを記述する