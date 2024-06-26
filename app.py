from flask import Flask, request, redirect, url_for, session, render_template
from facebook import GraphAPI

app = Flask(__name__)
app.secret_key = '6694cd47e3d9b5b01f02d78bfa2ad49c'
app_id = "925203059235069"
app_secret = "6694cd47e3d9b5b01f02d78bfa2ad49c"
redirect_uri = 'https://meta-meta.mg9com.easypanel.host/facebook/callback'

@app.route('/')
def home():
    return "Bem-vindo ao Sistema de Chat!"

@app.route('/login')
def login():
    permissions = 'email,public_profile,pages_show_list,pages_read_engagement,pages_manage_ads,pages_manage_metadata,pages_read_user_content,instagram_basic'
    return redirect(
        f"https://www.facebook.com/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&scope={permissions}"
    )

@app.route('/facebook/callback')
def facebook_callback():
    code = request.args.get('code')
    if code:
        graph = GraphAPI(version='3.1')
        access_token_info = graph.get_access_token_from_code(code, redirect_uri, app_id, app_secret)
        session['access_token'] = access_token_info['access_token']
        return redirect(url_for('dashboard'))
    return "Something went wrong!", 400

@app.route('/dashboard')
def dashboard():
    if 'access_token' not in session:
        return redirect(url_for('login'))
    graph = GraphAPI(access_token=session['access_token'], version='3.1')
    pages_data = graph.get_object('me/accounts')
    pages = pages_data.get('data', [])

    instagram_data = []
    for page in pages:
        insta_data = graph.get_object(f"{page['id']}", fields='instagram_business_account')
        if 'instagram_business_account' in insta_data:
            instagram_data.append(insta_data['instagram_business_account'])

    media_objects = []
    for insta in instagram_data:
        media_data = graph.get_object(f"{insta['id']}/media")
        media_objects.extend(media_data.get('data', []))

    return render_template('dashboard.html', pages=pages, instagram_accounts=instagram_data, media_objects=media_objects)

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
                return "Verification token mismatch", 403
        return "Bad request", 400

    elif request.method == 'POST':
        data = request.json
        print("Received webhook data:", data)
        # Aqui você pode processar a mensagem recebida, como armazenar em um banco de dados ou responder automaticamente
        return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(debug=True)
