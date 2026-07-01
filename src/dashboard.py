from flask import Flask, render_template_string, request
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import threading
from datetime import datetime



app = Flask(__name__)
app.config['SECRET_KEY'] = 'sisri2026'
socketio = SocketIO(app, cors_allowed_origins="*")

MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883
TOPICOS = ["semaforo/#", "detecao/#", "matriculas/#", "sisri/#", "#"]
mensagens = []
pub_client = None

def ao_conectar(client, userdata, flags, rc, properties=None):
    print(f"[MQTT] Conectado (rc={rc})")
    for t in TOPICOS:
        client.subscribe(t)

def ao_receber(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
    except:
        payload = str(msg.payload)
    entrada = {
        "topico": msg.topic,
        "payload": payload,
        "hora": datetime.now().strftime("%H:%M:%S"),
        "qos": msg.qos
    }
    mensagens.append(entrada)
    if len(mensagens) > 100:
        mensagens.pop(0)
    socketio.emit("nova_mensagem", entrada)
    print(f"[MQTT] {msg.topic} → {payload}")

def iniciar_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = ao_conectar
    client.on_message = ao_receber
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_forever()

HTML = """
<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8">
<title>SISRI-C.V Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/socket.io@4.7.5/dist/socket.io.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,sans-serif;background:#0f1117;color:#e2e8f0;min-height:100vh}
header{background:#1a1d27;border-bottom:1px solid #2d3148;padding:16px 24px;display:flex;align-items:center;justify-content:space-between}
h1{font-size:18px;font-weight:600;color:#fff}
h1 span{color:#4f8ef7}
.status{display:flex;align-items:center;gap:8px;font-size:13px;color:#94a3b8}
.dot{width:8px;height:8px;border-radius:50%;background:#22c55e;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.dot.off{background:#ef4444;animation:none}
main{padding:24px;max-width:900px;margin:0 auto}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:24px}
.card{background:#1a1d27;border:1px solid #2d3148;border-radius:10px;padding:16px}
.card-label{font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px}
.card-val{font-size:28px;font-weight:600;color:#fff}
.pub-box{background:#1a1d27;border:1px solid #2d3148;border-radius:10px;padding:16px;margin-bottom:24px}
.section-title{font-size:13px;font-weight:600;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px}
.row{display:flex;gap:10px;margin-bottom:10px;align-items:center}
.row label{font-size:12px;color:#64748b;min-width:70px}
.row input{flex:1;background:#0f1117;border:1px solid #2d3148;border-radius:6px;padding:7px 10px;color:#e2e8f0;font-size:13px;font-family:monospace}
.btn{padding:8px 20px;background:#4f8ef7;color:#fff;border:none;border-radius:6px;font-size:13px;font-weight:500;cursor:pointer}
.btn.red{background:#ef4444}
.log{background:#1a1d27;border:1px solid #2d3148;border-radius:10px;overflow:hidden}
.log-header{padding:12px 16px;border-bottom:1px solid #2d3148;display:flex;justify-content:space-between;align-items:center}
.log-body{max-height:400px;overflow-y:auto}
.msg{padding:10px 16px;border-bottom:1px solid #1e2235;display:grid;grid-template-columns:70px 1fr auto;gap:12px;font-size:13px}
.msg:hover{background:#1e2235}
.msg-hora{color:#4f8ef7;font-family:monospace;font-size:12px}
.msg-topico{font-family:monospace;color:#a78bfa;font-size:12px;margin-bottom:3px}
.msg-payload{color:#e2e8f0;word-break:break-all}
.msg-qos{font-size:10px;background:#2d3148;color:#94a3b8;padding:2px 6px;border-radius:4px}
.empty{padding:32px;text-align:center;color:#4a5568;font-size:13px}
</style>
</head>
<body>
<header>
  <h1>SISRI<span>-C.V</span> Dashboard MQTT</h1>
  <div class="status"><div class="dot" id="dot"></div><span id="status-txt">A ligar...</span></div>
</header>
<main>
  <div class="cards">
    <div class="card"><div class="card-label">Mensagens recebidas</div><div class="card-val" id="cnt-total">0</div></div>
    <div class="card"><div class="card-label">Broker</div><div class="card-val" style="font-size:15px;margin-top:4px">127.0.0.1:1883</div></div>
    <div class="card"><div class="card-label">Ultimo topico</div><div class="card-val" style="font-size:14px;margin-top:4px;color:#22c55e" id="ultimo-topico">—</div></div>
  </div>
  <div class="pub-box">
    <div class="section-title">Publicar mensagem</div>
    <div class="row"><label>Topico</label><input id="pub-topico" value="sisri/teste" /></div>
    <div class="row"><label>Mensagem</label><input id="pub-msg" value="{&quot;tipo&quot;:&quot;teste&quot;,&quot;valor&quot;:1}" /></div>
    <div style="display:flex;gap:8px">
      <button class="btn" onclick="publicar()">Publicar</button>
      <button class="btn red" onclick="limpar()">Limpar log</button>
    </div>
  </div>
  <div class="log">
    <div class="log-header">
      <div class="section-title" style="margin:0">Mensagens em tempo real</div>
      <span style="font-size:12px;color:#4a5568" id="cnt-label">0 mensagens</span>
    </div>
    <div class="log-body" id="log-body">
      <div class="empty" id="empty-msg">A aguardar mensagens MQTT...</div>
    </div>
  </div>
</main>
<script>
const socket = io();
let total = 0;
socket.on("connect", () => {
  document.getElementById("dot").classList.remove("off");
  document.getElementById("status-txt").textContent = "Dashboard ligado";
});
socket.on("disconnect", () => {
  document.getElementById("dot").classList.add("off");
  document.getElementById("status-txt").textContent = "Desligado";
});
socket.on("nova_mensagem", (d) => {
  total++;
  document.getElementById("cnt-total").textContent = total;
  document.getElementById("cnt-label").textContent = total + " mensagem" + (total !== 1 ? "s" : "");
  document.getElementById("ultimo-topico").textContent = d.topico;
  document.getElementById("empty-msg")?.remove();
  const body = document.getElementById("log-body");
  const div = document.createElement("div");
  div.className = "msg";
  div.innerHTML = `<div class="msg-hora">${d.hora}</div><div><div class="msg-topico">${d.topico}</div><div class="msg-payload">${d.payload}</div></div><div class="msg-qos">QoS ${d.qos}</div>`;
  body.insertBefore(div, body.firstChild);
});
function publicar() {
  const t = document.getElementById("pub-topico").value;
  const m = document.getElementById("pub-msg").value;
  fetch("/publicar", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify({topico:t, mensagem:m})});
}
function limpar() {
  document.getElementById("log-body").innerHTML = '<div class="empty" id="empty-msg">A aguardar mensagens MQTT...</div>';
  total = 0;
  document.getElementById("cnt-total").textContent = "0";
  document.getElementById("cnt-label").textContent = "0 mensagens";
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/publicar", methods=["POST"])
def publicar():
    data = request.get_json()
    pub_client.publish(data["topico"], data["mensagem"])
    return {"ok": True}

if __name__ == "__main__":
    pub_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    pub_client.connect(MQTT_HOST, MQTT_PORT, 60)
    pub_client.loop_start()
    t = threading.Thread(target=iniciar_mqtt, daemon=True)
    t.start()
    print("\n Dashboard SISRI a correr em http://localhost:5000\n")
    socketio.run(app, host="0.0.0.0", port=5000, debug=False, allow_unsafe_werkzeug=True)





    