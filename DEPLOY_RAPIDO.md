# 🚀 Deploy Rápido - Passo a Passo Simplificado

## ⚡ Opção Mais Fácil: Streamlit Cloud + Render

### 1️⃣ Preparar o Código (Já feito!)

✅ Backend já ajustado para variável `PORT`  
✅ Frontend já ajustado para variável `API_URL`  
✅ CORS configurado  
✅ Arquivos de deploy criados (`render.yaml`, `Procfile`)

---

### 2️⃣ Deploy do Backend (Render) - 5 minutos

1. **Acesse:** https://render.com
2. **Faça login** com GitHub
3. **Clique em:** "New" → "Web Service"
4. **Conecte seu repositório** GitHub
5. **Configure:**
   - **Name**: `alugai-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd api && python app.py`
   - **Plan**: Free (gratuito)
6. **Clique em:** "Create Web Service"
7. **Aguarde o deploy** (pode levar 2-5 minutos)
8. **Copie a URL** gerada (ex: `https://alugai-api.onrender.com`)

⚠️ **Importante:** Render pode ter "cold start" - a primeira requisição após inatividade pode demorar ~30 segundos.

---

### 3️⃣ Deploy do Frontend (Streamlit Cloud) - 3 minutos

1. **Acesse:** https://streamlit.io/cloud
2. **Faça login** com GitHub
3. **Clique em:** "New app"
4. **Configure:**
   - **Repository**: Seu repositório GitHub
   - **Branch**: `main` (ou `master`)
   - **Main file path**: `frontend/app.py`
5. **Clique em:** "Deploy"
6. **Após o deploy, configure Secrets:**
   - Vá em "Settings" → "Secrets"
   - Adicione:
     ```
     API_URL=https://alugai-api.onrender.com
     ```
   - (Substitua pela URL do seu backend no Render)
7. **Salve** e aguarde alguns segundos

---

### 4️⃣ Testar

1. **Backend:**
   ```bash
   curl https://seu-backend.onrender.com/health
   ```
   Deve retornar: `{"model_loaded": true, "status": "healthy"}`

2. **Frontend:**
   - Acesse a URL do Streamlit Cloud
   - Teste uma predição de preço
   - Verifique se conecta ao backend

---

## 🔧 Troubleshooting Rápido

### Backend não inicia:
- Verifique os logs no Render Dashboard
- Confirme que `requirements.txt` está completo
- Verifique se os modelos estão commitados (ou use storage externo)

### Frontend não conecta:
- Verifique se `API_URL` está configurada nos Secrets do Streamlit
- Teste a URL do backend diretamente no navegador
- Verifique os logs do Streamlit Cloud

### Modelo não carrega:
- Render não persiste arquivos entre deploys
- **Solução:** Commit os modelos no GitHub ou use S3/Cloud Storage

---

## 📝 Checklist Final

- [ ] Backend deployado no Render
- [ ] URL do backend copiada
- [ ] Frontend deployado no Streamlit Cloud
- [ ] `API_URL` configurada nos Secrets
- [ ] Teste de predição funcionando
- [ ] Logs verificados

---

## 🎉 Pronto!

Sua aplicação está no ar! 🚀

**URLs:**
- Frontend: `https://seu-app.streamlit.app`
- Backend: `https://alugai-api.onrender.com`

---

## 💡 Dicas Extras

1. **Manter Backend Ativo:**
   - Render pode "dormir" após inatividade
   - Use um serviço de ping (ex: UptimeRobot) para manter ativo

2. **Atualizar Código:**
   - Render: Deploy automático ao fazer push no GitHub
   - Streamlit Cloud: Deploy automático ao fazer push

3. **Monitoramento:**
   - Render Dashboard mostra métricas básicas
   - Streamlit Cloud mostra uso de recursos

---

**Precisa de ajuda?** Consulte `DEPLOY.md` para mais detalhes!

