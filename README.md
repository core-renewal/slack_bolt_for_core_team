# slack_bolt_for_core_team
.envファイルとUserList.pyはgitignoreしているのでローカルで準備する
### 環境変数
.envファイルに以下を設定する
- `SLACK_BOT_TOKEN`
- `SLACK_APP_TOKEN`
- `TARGET_CHANNEL_ID`
- `SLACK_SIGNING_SECRET`

### UserList
UserList.pyの中に
```
{
    "git user name":"slack user id",
    ...
}
```
の形式でリストを記述する