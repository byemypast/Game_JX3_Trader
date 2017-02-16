如何部署：
(a). 游戏设置
1. 首先你要有一台能运行剑三的机器
2. 将点卡充足的账号停在按F就能够到交易行商人的地方。强烈建议不要选择扬州、成都、太原等热门城市
3. 设置角色Ctrl + W为快速登出键

(b). 系统设置（win10通过）
1. 手动安装winio/winio64.sys(属性-->数字签名-->证书-->安装证书-->本地,放入下列存储：受信任的根)
2. 启动测试模式(管理员cmd: bcdedit /set testsigning on )
3. 重启
4. 如果你设置了“自动隐藏任务栏”，请取消
5. 将分辨率调整为1366*768

(c). 程序设置
1. 在目录下新建settings_pwd.py
输入：
USERNAME = "<你的游戏账号>"
PASSWORD = "<你的游戏密码>"

mail_host = "<你的邮箱STMP服务器>"（如"mail.pku.edu.cn"）
mail_user = "<你在此服务器下的账号>"（如"1xxxxxxxxx@pku.edu.cn"）
mail_pass = "<你在此服务器下的密码>"
保存

2.调整settings.py中头几行参数，通常你只用改动AHRECORD_FILENAME为你剑网三AH插件记录文件的位置即可。
这个文件通常位于游戏目录\\interface\\AH\\AH_Base\\data\\ah.jx3dat中

3.安装第三方库:pyperclip, Pillow, rabird.winio, win32api

(d).运行
1. 打开游戏，更新，并开始游戏至登录界面。（注意：每周一、周四的更新角色会不能上线，你需要手动停止脚本并更新后方可继续执行）
2. 使用管理员权限运行该脚本
3. 在10s内切换至剑网三窗口，并持续保持前台

(e).一些注意事项
1. 最好使用20级以下无点卡小号，避免消费点卡
2. 最好使用未满级小号，避免屠杀与仇杀。程序不内置回城等功能

(f).FUTURE
1. 买入卖出功能
2. 高级交易策略库
3. 分析物价功能
4. Django框架下的多权限可视化网站
5. 登录界面中的“服务器繁忙”状态

version 0.27
[+]进一步加强程序对1366*768的支持
version 0.26
[-]修复因游戏尚未加载出即执行进入交易行命令的BUG
version 0.25
[+]进一步加强程序对1366*768的支持
version 0.24
[+]增加服务器超时过滤功能
version 0.23
[-]修复了INT_GLOBAL_OVERTIME与INT_GLOBAL_WAITING冲突的问题
[-]现在程序由只支持1920*1080调整为只支持1366*768分辨率了
version 0.22
[+]增加DEBUG_FLAG, INT_GLOBAL_WAITING选项，方便调试与适应更多机器
[+]增加readme.txt中配置的一处注意事项
[-]修复一处发信模块的BUG
version 0.21
[+]将所有编码改为utf-8
version 0.2
[+]增加保存记录到数据库功能
[+]增加定时执行任务功能
[+]增加winio库
[+]增加readme
version 0.11
[-]修复readme.txt在github中显示不正常的bug
[-]修复在头几次询价中程序会错误打开风云榜的问题
[-]删除一些冗余代码
version 0.1
[+]自动查询功能完成