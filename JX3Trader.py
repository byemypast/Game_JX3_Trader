# -*- coding:gbk -*-  
import JX3Control
import time
from debug import *

#ONE TIME
import Onetime
Onetime.RecipeToItem()

time.sleep(5)
game = JX3Control.JX3Action()
game.login()
time.sleep(5)
game.openTrader()
time.sleep(5)
game.TraderSearchWithoutOCR_Online()
time.sleep(5)
game.logout()
result = game.TraderSearchWithoutOCR_Offline()
print(result)
debug(str(result))
debug(len(result))

