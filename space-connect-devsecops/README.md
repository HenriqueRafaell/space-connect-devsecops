# 🛰️ Space Connect - DevSecOps Implementation

[![Secret Detection](https://github.com/henrique-rafael/space-connect-devsecops/actions/workflows/secrets-scan.yml/badge.svg)](https://github.com/henrique-rafael/space-connect-devsecops/actions/workflows/secrets-scan.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Visão Geral

Este repositório contém uma implementação completa de **DevSecOps** para o projeto **Space Connect**, uma solução que processa dados satelitais, informações climáticas agrícolas e logística espacial.

### 🔐 Objetivo

Integrar segurança em todas as fases do pipeline CI/CD, desde o desenvolvimento local até a produção, garantindo:

- ✅ Proteção contra vazamento de credenciais
- ✅ Validação de vulnerabilidades em dependências
- ✅ Segurança em contêineres Docker
- ✅ Conformidade com LGPD e melhores práticas
- ✅ Rastreabilidade e auditoria contínua

---

## 🔒 Controles de Segurança Implementados

### 1. **Gestão de Segredos** 🔑
- **Ferramenta**: GitHub Secrets + detect-secrets
- **Objetivo**: Impedir vazamento de API keys, credenciais AWS e tokens
- **Onde entra**: Pre-commit hook (antes de fazer commit)
- **Status**: ✅ Ativo

### 2. **Análise Estática de Código (SAST)** 🔎
- **Ferramenta**: Bandit (para Python)
- **Objetivo**: Detectar vulnerabilidades de segurança no código
- **Onde entra**: Build stage (GitHub Actions)
- **Status**: ✅ Ativo

### 3. **Análise de Dependências** 📦
- **Ferramenta**: Safety CLI
- **Objetivo**: Encontrar bibliotecas com CVEs conhecidas
- **Onde entra**: Build stage (GitHub Actions)
- **Status**: ✅ Ativo

---

## 📁 Estrutura do Projeto

```
space-connect-devsecops/
├── .github/
│   └── workflows/
│       └── secrets-scan.yml          # GitHub Actions workflow
├── .githooks/
│   └── pre-commit                    # Pre-commit hook local
├── src/
│   ├── __init__.py
│   ├── config.py                     # Configuração segura do app
│   └── api_handler.py                # Integração com APIs externas
├── .detectsecrets.json               # Configuração do detect-secrets
├── .env.example                      # Template de variáveis de ambiente
├── .gitignore                        # Arquivos a ignorar no Git
├── README.md                         # Este arquivo
└── SECURITY.md                       # Guia de segurança detalhado
```

---

## 🚀 Como Usar Este Repositório

### 1️⃣ **Clone e Setup Inicial**

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/space-connect-devsecops.git
cd space-connect-devsecops

# Configure os pre-commit hooks
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit
```

### 2️⃣ **Instale as Dependências**

```bash
# Crie um virtual environment (opcional mas recomendado)
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as ferramentas de segurança
pip install detect-secrets bandit safety python-dotenv requests
```

### 3️⃣ **Configure as GitHub Secrets**

1. Acesse seu repositório no GitHub
2. Vá para **Settings → Secrets and variables → Actions**
3. Clique em **New repository secret**
4. Adicione os seguintes segredos:

| Secret Name | Valor de Teste |
|-------------|----------------|
| `SATELLITE_API_KEY` | `sk_test_satellite_demo_123456` |
| `AWS_ACCESS_KEY_ID` | `AKIA1234567890ABCDEF` |
| `AWS_SECRET_ACCESS_KEY` | `wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY` |
| `WEATHER_API_SECRET` | `weather_secret_test_xyz789` |
| `DATABASE_PASSWORD` | `db_password_test_secure_123` |
| `LOGISTICA_API_TOKEN` | `logistica_token_test_abc123` |

### 4️⃣ **Teste o Pre-commit Hook**

```bash
# Tente commitar (deve passar sem erros)
git add .
git commit -m "Initial setup"
```

✅ Se tudo funcionou, você verá:
```
🔍 Scanning for secrets before commit...
✅ No secrets detected. Proceeding with commit.
```

### 5️⃣ **Simule uma Falha de Segurança (Teste)**

```bash
# Abra o arquivo config.py e TEMPORARIAMENTE adicione uma API key:
# SATELLITE_API_KEY = "sk_live_fake_key_12345"

git add src/config.py
git commit -m "Test secret detection"

# Deve resultar em:
# ❌ SECRETS DETECTED! Commit aborted.
```

Depois reverta a mudança:
```bash
git restore src/config.py
git add src/config.py
git commit -m "Remove hardcoded secret"
```

---

## 📊 Verificando os Workflows

1. Faça um push para o repositório:
```bash
git push origin main
```

2. Vá para a aba **Actions** no GitHub
3. Clique em **Secret Detection**
4. Veja os logs do workflow executando

---

## 🔑 GitHub Secrets em Detalhes

### Como Usar os Secrets no Código

**ERRADO ❌** (Nunca faça assim):
```python
API_KEY = "sk_live_abc123def456"  # NUNCA commite secrets!
```

**CORRETO ✅** (Use variáveis de ambiente):
```python
import os
API_KEY = os.environ.get("SATELLITE_API_KEY")
```

### No GitHub Actions

Os secrets são acessados automaticamente:
```yaml
env:
  SATELLITE_API_KEY: ${{ secrets.SATELLITE_API_KEY }}
```

---

## 📖 Arquivos Importantes

### `.env.example`
Template de variáveis de ambiente para desenvolvimento local. Copie para `.env`:
```bash
cp .env.example .env
# Edite .env com valores reais (APENAS para desenvolvimento)
```

### `.detectsecrets.json`
Configuração das ferramentas de detecção de segredos. Detecta:
- AWS Keys
- GitHub Tokens
- Strings de alta entropia (possíveis segredos)
- Database credentials

### `.githooks/pre-commit`
Script executado antes de cada commit. Impede commits com segredos expostos.

---

## ✅ Checklist de Segurança

- [ ] GitHub Secrets configurados (6 secrets)
- [ ] Pre-commit hooks ativados (`git config core.hooksPath .githooks`)
- [ ] `.env.example` sem valores sensíveis
- [ ] Nenhum arquivo `.env` no repositório
- [ ] GitHub Actions workflows ativados
- [ ] `config.py` usando `os.environ.get()` para secrets
- [ ] Primeiro push com sucesso (Actions passando)

---

## 🧪 Testando os Controles

### Teste 1: Detecção de API Key
```bash
# Adicionar temporariamente ao código
echo 'API_KEY = "sk_live_test_123"' >> src/config.py
git add src/config.py
git commit -m "Test"
# Esperado: ❌ SECRETS DETECTED! Commit aborted.
```

### Teste 2: Usando Secrets Corretamente
```bash
# Usar variável de ambiente
echo 'API_KEY = os.environ.get("SATELLITE_API_KEY")' >> src/config.py
git add src/config.py
git commit -m "Use environment variable"
# Esperado: ✅ No secrets detected. Proceeding with commit.
```

### Teste 3: GitHub Actions Workflow
```bash
git push origin main
# Veja a aba Actions no GitHub
# Esperado: ✅ Secret Detection workflow passed
```

---

## 🐛 Troubleshooting

### Problema: Pre-commit hook não funciona
```bash
# Solução: Certificar que está executável
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks
```

### Problema: detect-secrets não instalado
```bash
# Solução: Instalar via pip
pip install detect-secrets
```

### Problema: GitHub Actions workflow falhando
1. Verifique se os Secrets estão configurados
2. Vá para **Settings → Actions → Workflow permissions**
3. Selecione **Read and write permissions**

---

## 📚 Documentação Adicional

- **[SECURITY.md](SECURITY.md)** - Guia completo de segurança
- **[.env.example](.env.example)** - Template de configuração
- **[src/config.py](src/config.py)** - Exemplo de código seguro

---

## 🎓 Trabalho Acadêmico

- **Aluno**: Henrique Rafael
- **RM**: 553945
- **Disciplina**: Cibersegurança 1 - FIAP
- **Professor**: MSc. Oerton Fernandes
- **Data**: 2026
- **Projeto**: Space Connect - DevSecOps Integration

---


