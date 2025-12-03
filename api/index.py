from flask import Flask, render_template, jsonify, send_from_directory
import os
from datetime import datetime

app = Flask(__name__, 
            static_folder='../static',
            template_folder='../templates')

CARTA_DADOS = {
    "destinatario": "Késsia",
    "subtitulo": "(Dona Kézia)",
    "autor": "Tiago",
    "data": datetime.now().strftime("%d de %B de %Y"),
    "conteudo": [
        {"paragrafo": "Quero expressar toda minha gratidão a senhora, que vai muito além das formalidades do dia a dia no trabalho. Às vezes, as palavras do cotidiano não são suficientes para expressar o que realmente sentimos, e hoje tive a oportunidade de lhe escrever o meu sincero 'obrigado'."},
        {"paragrafo": "Obrigado, primeiro, pela <span class='highlight'>liderança</span>. Por confiar em mim, por me desafiar com novos projetos e por acreditar no meu potencial mesmo quando eu próprio tinha dúvidas. Aprender com a sua experiência e visão tem sido um dos maiores trunfos da minha trajetória aqui."},
        {"paragrafo": "Mas este agradecimento é especial porque vai além. Quero agradecer pelos <span class='highlight'>conselhos</span> que vêm não só da chefe, mas da mulher sávia que você é. Pelas palavras de orientação nos momentos de indecisão, por me ensinar não apenas como fazer, mas o porquê das coisas. Obrigado pelo <span class='highlight'>apoio incondicional</span> por tantas vezes, especialmente quando as coisas ficavam turbulentas."},
        {"paragrafo": "Mas existe um detalhe ainda mais específico: o seu <span class='highlight'>cuidado</span> tem, muitas vezes, um acolhimento que lembra o de uma mãe. Essa preocupação genuína não só com o profissional que eu sou, mas com a pessoa que estou me tornando, que faz toda a diferença. Você cria um espaço onde é possível crescer, errar, aprender e seguir em frente, sentindo-se apoiado. Isso é um raro e precioso dom que a senhora tem."},
        {"paragrafo": "É uma <span class='highlight'>dádiva extraordinária</span> encontrar alguém que, como a senhora, também é uma mentora e uma verdadeira inspiração. Você moldou não apenas meu trabalho, mas também minha maneira de encarar os desafios e de me relacionar com os outros."},
        {"paragrafo": "Por tudo isso, do fundo do meu coração: <span class='highlight'>muito, muito obrigado</span>. É uma honra e um privilégio poder aprender e trabalhar ao seu lado."}
    ]
}

@app.route('/')
def index():
    return render_template('index.html', carta=CARTA_DADOS)

@app.route('/api/carta')
def api_carta():
    return jsonify(CARTA_DADOS)

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "carta-gratidao-kessia"
    })

# Servir arquivos estáticos
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# Handler para erros 404
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Handler para Vercel
def handler(request):
    from flask import request as flask_request
    with app.request_context(flask_request.environ):
        return app.full_dispatch_request()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)