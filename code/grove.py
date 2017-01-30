import time
import pyupm_grove as grove
import pyupm_i2clcd as lcd
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    msg=str("Flags de Conexao: " + str(flags) + "Codigo de Status: " + str(rc)
            + "Client_id: " + str(client))
    print(msg)

def on_publish(mosq, obj, mid):
    print("Mid: " + str(mid))

def on_log(client, user_data, level, buf):
    print("Log: ", buf)

# Dados de conexao MQTT
channel_id = "#youridchanel"
write_key = "#yourkey"
# Porta usada para link TCP
port = 1883
# Referencia do broker do ThingSpeak
broker = "mqtt.thingspeak.com"

client_mqtt = mqtt.Client("#yourinteledisonname")
client_mqtt.on_connect = on_connect
client_mqtt.on_publish = on_publish
client_mqtt.on_log = on_log

# Instanciacao de elementos Grove
led = grove.GroveLed(2)
button = grove.GroveButton(3)
temp = grove.GroveTemp(0)
glcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

glcd.clear()

# Instanciacao de variaveis usadas no programa
tempCelsius = 0
buttonStatus = 0
ledStatus = 0

# Apresentacao do programa
print("NodeGrove LHC Starting...")
glcd.write("Node LHC Start")

# Vamos mostrar o nome do LED
print("Componentes conectados: ")
print led.name()
print button.name()
print temp.name()

glcd.clear()
glcd.write("Node LHC Op")
# Vamos deixar o LED piscando indefinidamente...
while True:
    # Conexao ao Broker
    client_mqtt.connect(broker,port)
    # Inicia o mecanismo de conexao (leitura e escrita ao Broker)
    client_mqtt.loop_start()
    # Formato o link de acesso ao Broker do ThingSpeak
    url_link = str("channels/" + channel_id + "/publish/" + write_key)
    print("Url Link: " + url_link)
    # Faz o vinculo com o broker, usando a ID e Key
    client_mqtt.subscribe(url_link)
    # Formata a URL de "publicacao" dos dados
    url_publish = str("field1=" + str(buttonStatus) + "&field2=" + str(ledStatus)
            + "&field3=" + str(tempCelsius) + "&status=MQTTPUBLISH")
    print("Publicando MQTT: " + url_publish) 
    # Publicamos os dados no Broker MQTT ThingSpeak
    client_mqtt.publish(url_link, url_publish)
    # Todas as informacoes de variaveis
    # Sao carregadas no inicio do laco while
    tempCelsius = temp.value()

    glcd.setCursor(1,0)
    glcd.write("T:")
    glcd.write(str(tempCelsius))
    
    glcd.setCursor(1, 5)
    glcd.write("B:")
    glcd.write(str(buttonStatus))
    
    glcd.setCursor(1, 9)
    glcd.write("L:")
    glcd.write(str(ledStatus))

    buttonStatus = button.value()

    if buttonStatus:
        ledStatus = 1
        print("Botao pressionado")
        led.on()
        print("LED aceso")
    else:
        ledStatus = 0
        print("Botao liberado...")
        led.off()
        print("LED apagado")
    time.sleep(15)

# Remove o objeto para liberar memoria
del led
