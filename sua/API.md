### 由于nginx配置，以下url前全部加上/api
#### 提供给管理员的接口：
GET student/admin/
- 无需请求参数。
- 返回所有学生信息。
GET activity/admin/
- 无需请求参数。
- 返回所有活动信息。
GET sua/admin/
- 无需请求参数。
- 返回所有活动记录信息。
GET application/admin/
- 无需请求参数。
- 返回所有申请信息。
GET proof/admin/
- 无需请求参数。
- 返回所有证明信息。
#### 提供给普通学生的接口：
GET student/3
- 返回id为3的学生信息。
其余的以此类推。**注意，此时为方便，已经不用写?id=3了。**
POST auth/
{
    "status":0,
    "Remember_me":False,
    "username":19337001,
    "password":123,
}
成功时返回：
{
    "result":1,
    "id":19337001,
}
失败时返回；
{
    "result":0
}