# Teste - Brain Agriculture
Backend em Python/Django

## Tecnologias Utilizadas

- [Django](https://www.djangoproject.com/) - Framework web em Python.
- [Docker](https://www.docker.com/) - Plataforma para desenvolvimento e execução de aplicativos em contêineres.

## Pré-requisitos

Antes de começar, verifique se você possui as seguintes ferramentas instaladas:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Configuração do Ambiente

1. **Clone o repositório:**

```bash
git clone https://github.com/ejrgeek/teste-extractta-serasa
cd teste-extractta-serasa
```
   
2. **Construa e execute os contêineres**

O comando abaixo vai construir os contêineres necessários para o projeto e também executar comandos para migração, testes e execução do projeto.

```bash
docker-compose up --build
```
Caso haja a necessidade de recriar o banco após modificações na aplicação voce precisa para os contêineres com:
```bash
docker-compose down
```
Depois precisa recriá-los:
```bash
docker-compose up --build --force-recreate
```

3. **Criação de Superusuário**
```bash
docker-compose exec brain_agriculture python manage.py createsuperuser
```

4. **Rota para acessar aplicação**

Você poderá acessar a documentação das APIs por meio da URL abaixo, mas precisará logar.
```
http://127.0.0.1:8000/docs/
```

### Contribuição
Se você quiser contribuir com o projeto, siga estas etapas:

- Fork o projeto.
- Crie uma branch para sua feature (git checkout -b minha-feature).
- Faça commit das suas alterações (git commit -m 'Adiciona nova feature').
- Faça push para a branch (git push origin minha-feature).
- Abra um Pull Request.
