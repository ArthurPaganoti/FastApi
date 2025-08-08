# API de Usuários com FastAPI, MongoDB e JWT

Esta é uma API simples desenvolvida com FastAPI para cadastro, autenticação e gerenciamento de usuários, utilizando MongoDB como banco de dados e JWT para autenticação.

## Funcionalidades
- Cadastro de usuário (nome, e-mail, senha)
- Login com geração de token JWT
- Listagem de todos os usuários
- Busca de usuário por nome e por e-mail
- Atualização de e-mail e senha (autenticado)
- Exclusão de usuário (rota protegida por JWT)

## Tecnologias Utilizadas
- **FastAPI**
- **MongoDB** (via Motor)
- **Pydantic** (validação de dados)
- **Passlib** (hash de senha)
- **python-jose** (JWT)

## Segurança
- As rotas de exclusão e atualização de usuário exigem autenticação via token JWT.
- As senhas são armazenadas de forma criptografada.

Projeto simples para estudos e testes com FastAPI, MongoDB e autenticação JWT.

