# Discord Bot AI

Bot para Discord que utiliza modelos de linguagem natural (LLM) para responder perguntas dos usuários, integrando-se ao Ollama (Llama 3.2) e preparado para futuras integrações com OpenAI.

---

## Funcionalidades

- Responde perguntas enviadas no Discord via comando `!flok`.
- Cria threads automáticas para organizar conversas por usuário.
- Envia respostas por mensagem direta (DM), se permitido.
- Integração com modelo Ollama (Llama 3.2).
- Integração pronta para OpenAI (ChatGPT, GPT-4, etc).
- Estrutura modular para fácil expansão.
- Logs de atividades e erros para fácil depuração.
- Suporte a múltiplos modelos de linguagem.
- Fácil configuração via arquivo `.env`.
- Documentação gerada automaticamente com MkDocs.

---

## Pré-requisitos

- Python 3.10+
- Conta e servidor no Discord
- Acesso ao Ollama rodando localmente (ou endpoint configurado)
- Token de bot do Discord
- (Opcional) Chave de API da OpenAI para integração

---

## Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seuusuario/discord_botAI.git
   cd discord_botAI
   ```

2. **Crie o arquivo de variáveis de ambiente**
   - Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
     ```
     DISCORD_TOKEN='SEU_TOKEN_AQUI'
     # Para OpenAI (opcional)
     OPENAI_API_KEY='SUA_CHAVE_OPENAI'
     ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

---

## Uso

1. **Inicie o Ollama**  
   Certifique-se de que o Ollama está rodando localmente e o modelo Llama 3.2 está disponível.

2. **Execute o bot**
   ```bash
   python main.py
   ```

3. **No Discord**
   - Envie no canal:
     ```
     !flok Sua pergunta aqui
     ```
   - O bot irá responder e criar uma thread para a conversa.

---

## Documentação com MkDocs

Este projeto utiliza o [MkDocs](https://www.mkdocs.org/) para documentação.

### Instalar o MkDocs

```bash
pip install mkdocs
```

### Gerar e visualizar a documentação localmente

```bash
mkdocs serve
```

Acesse [http://localhost:8000](http://localhost:8000) no navegador para visualizar.

### Gerar documentação estática

```bash
mkdocs build
```

Os arquivos HTML serão gerados na pasta `site/`.

---

## Estrutura do Projeto

```
discord_botAI/
│
├── main.py                        # Arquivo principal do bot
├── requirements.txt               # Dependências do projeto
├── .env                           # Variáveis de ambiente (não versionado)
├── /docs                          # Documentação do projeto (MkDocs)
│   └── index.md
├── /src                           # Código-fonte modularizado
│   ├── bot.py                     # Lógica do bot Discord
│   ├── ollama_bot.py              # Integração com Ollama
│   ├── OpenAi_API/
│   │   └── openai_bot.py          # Integração com OpenAI
│   └── utils.py                   # Funções utilitárias
└── README.md                      # Resumo do projeto
```

---

## Configuração Avançada

- Para integrar com outros LLMs (ex: OpenAI), adicione as credenciais e endpoints necessários no `.env` e implemente novos clientes em `/src`.
- Permissões do bot: certifique-se de que o bot tem permissão para ler, escrever e criar threads no canal desejado.
- Para alternar entre modelos (Ollama ou OpenAI), ajuste a configuração no código principal.

---

## Contribuição

1. Fork este repositório
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas alterações (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## Licença

MIT

---

## Contato

Dúvidas ou sugestões? Abra uma issue ou envie um e-mail para [seuemail@dominio.com](mailto:seuemail@dominio.com).
