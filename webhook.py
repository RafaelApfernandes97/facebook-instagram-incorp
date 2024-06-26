from flask import Flask, request, jsonify, abort

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verificação do Webhook
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode and token:
            if mode == 'subscribe' and token == '6694cd47e3d9b5b01f02d78bfa2ad49c':
                print("WEBHOOK_VERIFIED")
                return challenge
            else:
                abort(403)
        abort(400)

    elif request.method == 'POST':
        data = request.json
        print("Received webhook data:", data)

        # Processa a notificação
        # Aqui você pode adicionar lógica para responder a mensagens ou eventos
        # Por exemplo, analisar `data['entry'][0]['messaging'][0]['message']['text']`
        
        return 'EVENT_RECEIVED', 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
