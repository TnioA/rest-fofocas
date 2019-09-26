# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests
import json
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/api/fofocas', methods=['GET'])
def getfofocas():
	html_doc = requests.get('https://tvefamosos.uol.com.br/')
	
	soup = BeautifulSoup(html_doc.text, 'html.parser')
    	

	##    Blocos    ##
	destaques = soup.find('section', class_='highlights-with-photo').find('div', class_='row')
	padroes = soup.find_all('section', class_='highlights-headline')
	ultimas = soup.find('section', class_='latest-news')
	data = []
	fofocas = []
	ultimas_noticias = []

	#print(ultimas)

	for dataBox_destaques in destaques.find_all('div', class_='thumbnail-standard'):
		imgdestaques = dataBox_destaques.find('img')
		title = dataBox_destaques.find('span', class_='thumb-kicker')
		content = dataBox_destaques.find('h3', class_='thumb-title').text
		content = content.replace('\"', '')

		#tratamento-url-imagem
		##urlimg = imgdestaques['src'].replace('jpgx', 'jpg')
		urlimg = imgdestaques['data-src']

		data.append({'imagem' : urlimg, 'titulo' : title.text.strip(),'conteudo' : content.strip()})

	for dataBox_padroes in padroes:
		if dataBox_padroes.find('div', class_='section-title'):
			padrao_titulo = dataBox_padroes.find('div', class_='section-title').find('span').text
		else:
			padrao_titulo = ''

		#print(padrao_titulo)
		imgitens = []
		textitens = []
		conteudo = []
		c = 0
		for getcontent in dataBox_padroes.find_all('div', class_='thumbnail-standard'):
			imgpadroes = getcontent.find('img')
			textpadroes = getcontent.find('a').find('h3').text.strip()

			# tratamento imagem
			imgitem = imgpadroes['data-src'].replace('jpgx', 'jpg')

			conteudo.append({'imagem' : imgitem, 'conteudo' : textpadroes})


		#conteudo.append({'primeiro-conteudo' : textitens[0], 'primeiro-imagem' : imgitens[0]['src'], 'segundo-conteudo' : textitens[1], 'terceiro-conteudo' : textitens[2], 'quarto-conteudo' : textitens[3]})
		fofocas.append({'titulo' : padrao_titulo.strip(), 'conteudo' : conteudo})
			

	for dataBox_ultimas in ultimas.find_all('div', class_='thumbnail-standard'):
		if dataBox_ultimas.find('h3', class_='thumb-title'):
			imgultimas = dataBox_ultimas.find('img')
			content = dataBox_ultimas.find('h3', class_='thumb-title').text
			content = content.replace('\"', '')
			data_ultimas = dataBox_ultimas.find('time', class_='thumb-time')

			if (hasattr(imgultimas, 'src')):
				aux = imgultimas['data-src']
			else:
				aux = ''

			#tratamento-url-imagem
			aux = aux.replace('jpgx', 'jpg')

			ultimas_noticias.append({'imagem' :  aux,'conteudo' : content.strip(),'data' : data_ultimas.text.strip()})


	return jsonify({'destaques' : data, 'fofocas' : fofocas, 'ultimas' : ultimas_noticias})
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

