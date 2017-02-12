# -*- coding:gbk -*-  
import JX3Control
import time

time.sleep(5)
game = JX3Control.JX3Action()
game.login("wangjunyi2008@hsc.pku.edu.cn","pkueecs2012")
time.sleep(5)
game.logout()