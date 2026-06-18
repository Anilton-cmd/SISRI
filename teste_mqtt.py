
import paho.mqtt.client as mqtt

def ao_conectar(client, userdata, flags, rc, properties=None):
    print("✅ Conectado ao broker MQTT!")
    client.subscribe("semaforo/teste")
    client.publish("semaforo/teste", "Olá do SISRI-C.V!")  # ← aqui dentro!

def ao_receber(client, userdata, msg):
    print(f"📨 Mensagem recebida: {msg.payload.decode()}")



client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = ao_conectar
client.on_message = ao_receber

client.connect("127.0.0.1", 1883)
client.loop_forever()
