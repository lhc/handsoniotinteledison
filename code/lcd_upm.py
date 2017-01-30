import pyupm_i2clcd as lcd
import time

import socket
from urllib2 import urlopen, URLError, HTTPError

# SetDefaultTimetou - Tudo em minusculo!
socket.setdefaulttimeout(5)

url = 'http://w.ggle.com.br'

#i2c lcd   bkl 
glcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

# Limpa o display
glcd.clear()

# Seta a cor - Branco!
glcd.setColor(255,255,255)

# Posiciona o cursor do display - 16x2
glcd.setCursor(0, 0)

glcd.write("Ola mundo")

while True:
    try:
        response = urlopen(url) # Tenta conectar no Google!
    except HTTPError, e:
        glcd.clear()
        glcd.setColor(255,0,0) #LCD em Vermelho
        glcd.write("Google Out")
    except URLError, e:
        glcd.clear()
        glcd.setColor(255,0,0)
        glcd.write("Google Out")
    else:
        glcd.clear()
        html = response.read() # leitura de resposta do site com sucesso
        glcd.setColor(0,255,0)
        glcd.write("Google OK!")
    time.sleep(1)
