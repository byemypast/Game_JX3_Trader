# -*- coding:gbk -*-  
import JX3Control
import time

time.sleep(5)
game = JX3Control.JX3Action()
game.login("user","pwd")
time.sleep(5)
game.logout()