# 🚀 Guia de Deploy - AlugAI

Este guia apresenta as opções mais fáceis para fazer deploy da aplicação AlugAI.

## 📋 Estrutura da Aplicação

- **Frontend**: Streamlit (Python)
- **Backend**: Flask API (Python)
- **ML Model**: XGBoost (arquivos pickle)

---

## 🎯 Opção 1: Streamlit Cloud (Frontend) + Render (Backend) ⭐ RECOMENDADO

### **Frontend - Streamlit Cloud** (GRATUITO)

**Por que usar:**
- ✅ Totalmente gratuito
- ✅ Deploy em 2 minutos
- ✅ Integração nativa com Streamlit
- ✅ HTTPS automático
- ✅ Atualização automática via GitHub

**Passos:**

1. **Criar conta no Streamlit Cloud:**
   - Acesse: https://streamlit.io/cloud
   - Faça login com GitHub

2. **Preparar repositório:**
   ```bash
   # Certifique-se de que o frontend tem requirements.txt
   cd frontend
   # O requirements.txt já existe
   ```

3. **Fazer deploy:**
   - No Streamlit Cloud, clique em "New app"
   - Conecte seu repositório GitHub
   - Selecione o branch (geralmente `main` ou `master`)
   - **Main file path**: `frontend/app.py`
   - Clique em "Deploy"

4. **Configurar variáveis de ambiente:**
   - No Streamlit Cloud, vá em "Settings" → "Secrets"
   - Adicione a URL da API do backend:
   ```
   API_URL=https://seu-backend.onrender.com
   ```

---

### **Backend - Render** (GRATUITO)

**Por que usar:**
- ✅ Plano gratuito disponível
- ✅ Deploy automático via GitHub
- ✅ HTTPS automático
- ✅ Fácil configuração

**Passos:**

1. **Criar conta no Render:**
   - Acesse: https://render.com
   - Faça login com GitHub

2. **Preparar arquivos de deploy:**

   Crie `backend/render.yaml`:
   ```yaml
   services:
     - type: web
       name: alugai-api
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: cd api && python app.py
       envVars:
         - key: PORT
           value: 5020
   ```

   Ou crie `backend/api/Procfile`:
   ```
   web: cd api && python app.py
   ```

3. **Ajustar código para Render:**

   No `backend/api/app.py`, modifique a última linha:
   ```python
   if __name__ == '__main__':
       port = int(os.environ.get('PORT', 5020))
       app.run(host='0.0.0.0', port=port, debug=False)
   ```

4. **Fazer deploy:**
   - No Render, clique em "New" → "Web Service"
   - Conecte seu repositório GitHub
   - Configure:
     - **Name**: `alugai-api`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `cd api && python app.py`
   - Clique em "Create Web Service"

5. **Upload do modelo:**
   - Render não persiste arquivos entre deploys
   - Opções:
     a) **Usar GitHub**: Commit os arquivos do modelo em `backend/models/`
     b) **Usar S3/Cloud Storage**: Modificar código para baixar do S3
     c) **Usar variável de ambiente**: Base64 encode do modelo (não recomendado)

---

## 🎯 Opção 2: Railway (Ambos) ⭐ ALTERNATIVA

**Por que usar:**
- ✅ Plano gratuito ($5/mês de crédito)
- ✅ Deploy muito simples
- ✅ Suporta ambos frontend e backend
- ✅ Persistência de arquivos

**Passos:**

1. **Criar conta:**
   - Acesse: https://railway.app
   - Faça login com GitHub

2. **Deploy do Backend:**
   - Clique em "New Project" → "Deploy from GitHub repo"
   - Selecione seu repositório
   - Railway detecta automaticamente Python
   - Configure:
     - **Root Directory**: `backend`
     - **Start Command**: `cd api && python app.py`
   - Adicione variável de ambiente: `PORT=5020`

3. **Deploy do Frontend:**
   - Crie outro serviço no mesmo projeto
   - **Root Directory**: `frontend`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

4. **Upload do modelo:**
   - Railway persiste arquivos
   - Faça upload via CLI ou interface web

---

## 🎯 Opção 3: Fly.io (Ambos)

**Por que usar:**
- ✅ Plano gratuito generoso
- ✅ Deploy via CLI
- ✅ Muito rápido

**Passos:**

1. **Instalar Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login:**
   ```bash
   fly auth login
   ```

3. **Deploy Backend:**
   ```bash
   cd backend
   fly launch
   # Siga as instruções
   ```

4. **Deploy Frontend:**
   ```bash
   cd frontend
   fly launch
   ```

---

## 🔧 Ajustes Necessários no Código

### 1. Backend - Suportar variável PORT

Modifique `backend/api/app.py`:

```python
import os

# No final do arquivo:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5020))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
```

### 2. Frontend - Usar URL da API dinâmica

Modifique `frontend/pages/estimativa_preco.py` e outros:

```python
import os

# No início do arquivo:
API_URL = os.environ.get('API_URL', 'http://localhost:5020')
```

### 3. CORS - Permitir domínio do frontend

No `backend/api/app.py`, ajuste CORS:

```python
from flask_cors import CORS

# Permitir domínio do Streamlit Cloud
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://*.streamlit.app",
            "http://localhost:8501"
        ]
    }
})
```

---

## 📦 Preparação dos Arquivos

### 1. Criar `.gitignore` (se não existir)

```
# Modelos ML
backend/models/*.pkl
backend/models/*.json
!backend/models/.gitkeep

# Logs
*.log
/tmp/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

### 2. Commit dos modelos (se usar GitHub)

```bash
# Se quiser versionar os modelos:
git add backend/models/*.pkl backend/models/*.json
git commit -m "Add trained models"
git push
```

**⚠️ Atenção:** Modelos podem ser grandes. Considere usar Git LFS:
```bash
git lfs install
git lfs track "*.pkl"
git add .gitattributes
```

---

## 🚀 Deploy Rápido (Streamlit Cloud + Render)

### Passo a Passo Simplificado:

1. **Backend (Render):**
   ```bash
   # 1. Commit e push do código
   git add .
   git commit -m "Prepare for deploy"
   git push origin main
   
   # 2. No Render:
   # - New Web Service
   # - Connect GitHub
   # - Build: pip install -r requirements.txt
   # - Start: cd api && python app.py
   # - Anote a URL gerada (ex: https://alugai-api.onrender.com)
   ```

2. **Frontend (Streamlit Cloud):**
   ```bash
   # 1. No Streamlit Cloud:
   # - New app
   # - Connect GitHub
   # - Main file: frontend/app.py
   # - Em Secrets, adicione:
   #   API_URL=https://alugai-api.onrender.com
   ```

3. **Atualizar Frontend:**
   - Modifique `frontend/pages/estimativa_preco.py`:
   ```python
   import os
   API_URL = os.getenv('API_URL', 'http://localhost:5020')
   ```

---

## 🔍 Verificação Pós-Deploy

1. **Testar Backend:**
   ```bash
   curl https://seu-backend.onrender.com/health
   ```

2. **Testar Frontend:**
   - Acesse a URL do Streamlit Cloud
   - Teste uma predição

3. **Verificar Logs:**
   - Render: Dashboard → Logs
   - Streamlit Cloud: Settings → Logs

---

## 💡 Dicas Importantes

1. **Modelos grandes:**
   - Se os modelos forem > 100MB, considere usar S3/Cloud Storage
   - Render tem limite de 500MB no plano gratuito

2. **Cold Start:**
   - Render pode ter "cold start" (primeira requisição demora)
   - Considere usar um serviço de "ping" para manter ativo

3. **Variáveis de Ambiente:**
   - Nunca commite secrets no código
   - Use variáveis de ambiente sempre

4. **Monitoramento:**
   - Render oferece métricas básicas
   - Streamlit Cloud mostra uso de recursos

---

## 🆘 Troubleshooting

### Backend não inicia:
- Verifique os logs no Render
- Confirme que `requirements.txt` está completo
- Verifique se o modelo está no caminho correto

### Frontend não conecta ao backend:
- Verifique CORS no backend
- Confirme que `API_URL` está configurada corretamente
- Teste a URL do backend diretamente

### Modelo não carrega:
- Verifique se os arquivos estão commitados
- Confirme o caminho relativo no código
- Considere usar caminho absoluto ou variável de ambiente

---

## 📚 Recursos Úteis

- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app
- **Fly.io Docs**: https://fly.io/docs

---

## ✅ Checklist de Deploy

- [ ] Código commitado no GitHub
- [ ] `requirements.txt` atualizado
- [ ] Backend ajustado para variável `PORT`
- [ ] Frontend ajustado para `API_URL` dinâmica
- [ ] CORS configurado no backend
- [ ] Modelos commitados ou em storage
- [ ] Variáveis de ambiente configuradas
- [ ] Testes realizados localmente
- [ ] Deploy do backend realizado
- [ ] Deploy do frontend realizado
- [ ] Testes pós-deploy realizados

---

**Boa sorte com o deploy! 🚀**

