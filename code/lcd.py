import pyupm_i2clcd as lcd
import time

lcdDisplay = lcd.Jhd1313m1(0, 0x3E, 0x62)

lcdDisplay.setCursor(0, 0)
lcdDisplay.write("HandsOn IoT")
lcdDisplay.setCursor(1,0)
lcdDisplay.write("IntelEdison LHC")
while True:
	time.sleep(1)
