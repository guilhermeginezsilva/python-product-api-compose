# API de CRUD de produtos

Este microserviço é um CRUD de produtos feito em python

## Como rodar localhost?
Para rodar o projeto é necessário ter instalado o docker e o docker-compose. O projeto já está configurado com um arquivo docker-compose, desta forma é necessário apenas:

1. Navegar até a pasta raiz deste repositório

2. Buildar a imagem do python

		docker build -t python-products-api:v1 ./products-api

2. Buildar o docker-compose

		docker-compose build

3. Rodar o docker-compose

		docker-compose up

4. O docker compose vai subir tanto o banco de dados quanto a aplicação.
O banco de dados responde na porta 3306 e a aplicação na porta 8080.

## Como rodar na AWS?

Apenas siga os passos abaixo e selecione as variáveis de ambiente AWS ao invés de local no postman. Foi disponibilizado um load balancer na amazon já configurado com a aplicação.

## Como chamar as rotas?

Para chamar as rotas é necessário alguma ferramenta que faça chamadas REST e também um token válido JWT. Para isso:

1. Faça login na página abaixo:

	https://product-api-auth.s3.amazonaws.com/auth.html

2. Copie o token gerado

3. Para ajudar na chamada das APIs estou disponibilizando uma coleção de chamadas da aplicação postman já configurada com as rotas. Faça o download aqui da coleção e das variáveis de ambiente:

	Coleção com requests locais:

	https://product-api-auth.s3.amazonaws.com/postman/Python+Product+API.postman_collection.json

	Variáveis de ambiente para rodar local:

	https://product-api-auth.s3.amazonaws.com/postman/Local.postman_environment.json

	Coleção com requests do API Gateway da AWS:

	https://product-api-auth.s3.amazonaws.com/postman/Python+Product+API+-+API+Gateway.postman_collection.json

	Variáveis de ambiente para rodar com a AWS:

	https://product-api-auth.s3.amazonaws.com/postman/AWS+Dev.postman_environment.json

4. Pegue o token copiado do passo 2 e substitua na variável de ambiente local e aws do postman, variável access-token

5. Pronto, o ambiente está configurado

## Como rodar os testes?

1. Para rodar os testes navegue até a pasta do projeto:

		cd ./products-api

2. Execute o comando abaixo, para isso é necessário ter o python 3.7 instalado na máquina:

		python -m unittest -v

## Arquitetura do projeto:
O projeto é um CRUD e está dividido em:
	
* Inicializador da aplicação que também é o controller que recebe as requisições
	
* Serviço de produtos contendo as regras de negócio

* DAO de produtos para acessar o banco de dados

* Utilitários de segurança para validar o token JWT e de gerenciamento das variáveis de ambiente utilizadas pela aplicação

Frameworks e bibliotecas:

* Fastapi: foi utilizado para fazer o controle das requisições

* Exceptions (fontes locais): para padronizar as respostas de erro e ter mais controle sobre as mensagens

* Validators (fontes locais): para conseguir integrar as validações com o mecanismo de exceptions

* Cognitojwt: Para autenticar o token do usuário na AWS

## Regras:

Criar uma API com os seguintes endpoints:

* **GET /produtos**: Retorna uma lista de produtos.

* **GET /produtos/:id**: Retorna um produto específico.

* **POST /produtos**: Cria um novo produto.

* **PUT/PATCH /produtos/:id**: Permite a alteração de um produto específico.

* **DELETE /produtos/:id**: Permitir a exclusão de um produto específico.


A comunicação entre a API e o cliente deve ser realizada por intermédio de JSON e estes dados devem ser persistidos em um banco de dados.

O schema de dados é:
nome

	tipo: string
	comprimento entre 3 e 50 caracteres
	não pode ser nulo
	não pode começar ou terminar com letras

categoria

	tipo: array
	valores permitidos:
	eletrônicos
	utensílios
	cama e mesa
	cozinha
	higiene pessoal
	abobrinha
	pode ser cadastrada mais de uma categoria

preço

	tipo: float
	intervalo de valores entre 1.99 a 5000.00
	valor pode ser nulo

url

	tipo: string
	comprimento de caracteres entre 30 e 120
	não pode ser nulo
	url deve ser a hifenização do nome do produto mais a url que eu desejo

Pontos que devem constar:

* Autenticação usando JWT - OK
* Validação de JSON e campos - OK
* Mensagem de erros personalizadas - OK
* Disponibilizar a API em serviços de hospedagem, tais como: Heroku,  Azure, AWS, etc. - OK
* Habilitação de CORS - OK

Pontos extras:

* Criar uma interface front-end para consumo da API - Pendente
* Utilizar uma framework SPA, tal como: React, Vue ou Angular. - Pendente
* Criar layout responsivo na interface front-end - Pendente
* Habilitação de SSL com nota mínima A validado pelo site * https://www.ssllabs.com/ssltest/index.html - OK
* Segurança de cabeçalhos com nota mínima B no site https://* securityheaders.com/ - Pendente
* Performance grade mínima de 85 no site https://* tools.pingdom.com/ - OK
