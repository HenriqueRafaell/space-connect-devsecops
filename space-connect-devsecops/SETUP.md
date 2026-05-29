# 🚀 SETUP.md - Instruções de Configuração

Este arquivo contém instruções **passo a passo** para configurar o repositório.

---

## 📋 Checklist Rápido

- [ ] GitHub Secrets configurados (6 secrets)
- [ ] Pre-commit hooks ativados
- [ ] Primeiro commit funcionando
- [ ] GitHub Actions workflow passando
- [ ] Projeto pronto para entrega

---

## ⏱️ Tempo Total: ~15 minutos

---

## Passo 1: Clonar e Preparar (2 min)

```bash
# 1.1 Clone o repositório (já deve estar clonado)
cd space-connect-devsecops

# 1.2 Instale Python 3.11+ (se necessário)
python3 --version  # Deve ser 3.11+

# 1.3 Crie virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 1.4 Instale dependências
pip install detect-secrets bandit safety python-dotenv requests
```

---

## Passo 2: Configurar GitHub Secrets (5 min)

### No GitHub.com

1. **Acesse seu repositório**
2. **Settings** → **Secrets and variables** → **Actions**
3. Clique em **New repository secret**
4. **Adicione um a um:**

```
Nome: SATELLITE_API_KEY
Valor: sk_test_satellite_demo_123456

Nome: AWS_ACCESS_KEY_ID
Valor: AKIA1234567890ABCDEF

Nome: AWS_SECRET_ACCESS_KEY
Valor: wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY

Nome: WEATHER_API_SECRET
Valor: weather_secret_test_xyz789

Nome: DATABASE_PASSWORD
Valor: db_password_test_secure_123

Nome: LOGISTICA_API_TOKEN
Valor: logistica_token_test_abc123
```

✅ **Depois de adicionar todos 6 secrets**, continue.

---

## Passo 3: Configurar Pre-commit Hooks (2 min)

```bash
# 3.1 Configure git para usar .githooks
git config core.hooksPath .githooks

# 3.2 Deixe o pre-commit executável
chmod +x .githooks/pre-commit

# 3.3 Verifique se funcionou
ls -la .githooks/pre-commit  # Deve ter "x" (executável)
```

---

## Passo 4: Primeiro Commit (3 min)

```bash
# 4.1 Verifique o status
git status

# 4.2 Adicione todos os arquivos
git add .

# 4.3 Faça o commit
git commit -m "Initial DevSecOps setup"

# Esperado:
# 🔍 Scanning for secrets before commit...
# ✅ No secrets detected. Proceeding with commit.
```

Se passar, você verá:
```
[main abcd1234] Initial DevSecOps setup
 X files changed, Y insertions(+)
```

---

## Passo 5: Push para GitHub (2 min)

```bash
# 5.1 Push das mudanças
git push origin main

# 5.2 Verifique se o workflow rodou
# Vá para: GitHub → Actions → Secret Detection
```

---

## Passo 6: Testar Detecção de Segredos (3 min)

### Teste 1: Simular Vazamento

```bash
# 6.1 Abra o arquivo src/config.py
# Adicione TEMPORARIAMENTE uma linha com segredo:

# ADICIONE ISTO TEMPORARIAMENTE:
TEST_SECRET = "sk_live_fake_key_12345"

# 6.2 Tente commitar
git add src/config.py
git commit -m "Test secret detection"

# Esperado:
# ❌ SECRETS DETECTED! Commit aborted.
```

### Teste 2: Remover e Commitar Corretamente

```bash
# 6.3 Remova a linha que adicionou (delete TEST_SECRET)
# Coloque de volta como estava

# 6.4 Tente commitar novamente
git add src/config.py
git commit -m "Remove test secret"

# Esperado:
# ✅ No secrets detected. Proceeding with commit.
```

---

## Passo 7: Validar Workflows (3 min)

### No GitHub

1. **Vá para Actions**
2. **Clique em "Secret Detection"**
3. **Clique no último workflow**
4. Verifique se passou ✅

### Esperado Ver

- ✅ Secret Detection: PASSED
- ✅ SAST Scan: PASSED
- ✅ Summary: All security checks completed!

---

## 🎯 Pronto!

Se todos os passos passaram:

```
✅ Pre-commit hooks configurados
✅ GitHub Secrets cadastrados
✅ Primeiro commit funcionando
✅ GitHub Actions workflows passando
✅ Detecção de segredos testada
```

---

## ❌ Troubleshooting

### Problema: "detect-secrets: command not found"

```bash
# Solução
pip install detect-secrets
```

### Problema: Pre-commit hook não executa

```bash
# Solução
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks
```

### Problema: GitHub Actions workflow falhou

1. Verifique se os 6 secrets estão configurados
2. Vá para **Settings → Actions → Workflow permissions**
3. Selecione **Read and write permissions**
4. Push novamente: `git push origin main`

### Problema: "Permission denied .githooks/pre-commit"

```bash
# Solução
chmod +x .githooks/pre-commit
```

---

## 📝 Próximos Passos

1. **Leia o README.md** para entender o projeto
2. **Leia o SECURITY.md** para boas práticas
3. **Prepare suas evidências** (screenshots)

---

## 📸 Screenshots para Entrega

Tire prints dos seguintes itens:

1. **GitHub Secrets configurados**
   - Settings → Secrets and variables → Actions
   - Mostrar lista de 6 secrets

2. **Pre-commit hook funcionando**
   - Terminal mostrando: "✅ No secrets detected"

3. **GitHub Actions workflow passando**
   - Actions → Secret Detection → mostrando ✅ PASSED

4. **Estrutura do repositório**
   - Code → mostrando os arquivos (config.py, api_handler.py, etc)

5. **Simularção de detecção**
   - Terminal mostrando commit sendo bloqueado por segredo
   - Depois mostrando commit sendo aceito após correção

---

## ✨ Você está pronto!

Se tudo funcionou, o repositório está seguro e pronto para ser entregue.

**Parabéns! 🎉**

