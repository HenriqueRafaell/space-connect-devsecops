# 🔐 SECURITY.md - Guia de Segurança DevSecOps

Este documento detalha todos os controles de segurança implementados no Space Connect.

---

## 📋 Índice

1. [Gestão de Segredos](#gestão-de-segredos)
2. [Detecção de Vulnerabilidades](#detecção-de-vulnerabilidades)
3. [Pre-commit Hooks](#pre-commit-hooks)
4. [GitHub Actions Workflows](#github-actions-workflows)
5. [Boas Práticas](#boas-práticas)
6. [Resposta a Incidentes](#resposta-a-incidentes)

---

## Gestão de Segredos

### GitHub Secrets

GitHub Secrets é o método recomendado para armazenar credenciais sensíveis.

#### Como Configurar

1. **Settings → Secrets and variables → Actions**
2. **New repository secret**
3. Adicione o nome e valor

#### Secrets Necessários para Space Connect

| Nome | Tipo | Descrição |
|------|------|-----------|
| `SATELLITE_API_KEY` | API Key | Acesso à API de satélites |
| `AWS_ACCESS_KEY_ID` | AWS Credential | ID da chave AWS |
| `AWS_SECRET_ACCESS_KEY` | AWS Credential | Chave secreta AWS |
| `WEATHER_API_SECRET` | API Secret | Token da API de clima |
| `DATABASE_PASSWORD` | Credential | Senha do banco de dados |
| `LOGISTICA_API_TOKEN` | Token | Token da API de logística |

#### Como Usar no Código

```python
import os

# ERRADO ❌
api_key = "sk_live_abc123"  # NUNCA!

# CORRETO ✅
api_key = os.environ.get("SATELLITE_API_KEY")

# COM VALOR PADRÃO
database_host = os.environ.get("DATABASE_HOST", "localhost")
```

#### Como Usar no GitHub Actions

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        env:
          SATELLITE_API_KEY: ${{ secrets.SATELLITE_API_KEY }}
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        run: ./deploy.sh
```

---

## Detecção de Vulnerabilidades

### detect-secrets

Ferramenta que detecta segredos hardcoded no código.

#### Detecções Implementadas

- ✅ AWS Keys (AKIA...)
- ✅ GitHub Tokens (ghp_...)
- ✅ Database Passwords
- ✅ API Keys genéricas
- ✅ Strings com alta entropia

#### Como Usar

```bash
# Scan inicial
detect-secrets scan > .detectsecrets.json

# Auditar baseline
detect-secrets audit .detectsecrets.json

# Scan simples
detect-secrets scan --baseline .detectsecrets.json
```

### Bandit (SAST)

Analisador estático de segurança para Python.

#### Vulnerabilidades Detectadas

- SQL Injection risks
- Use of insecure cryptographic functions
- Hardcoded passwords
- Insecure random functions
- Insecure deserialization

#### Como Usar

```bash
# Scan do código
bandit -r src/ -f json -o bandit-report.json

# Scan com detalhes
bandit -r src/ -ll  # Low level details
```

### Safety

Verifica dependências Python contra banco de dados de CVEs.

#### Como Usar

```bash
# Check de dependências
safety check --json

# Contra arquivo específico
safety check -r requirements.txt
```

---

## Pre-commit Hooks

O arquivo `.githooks/pre-commit` executa antes de cada commit, impedindo que segredos sejam commitados.

### Como Ativar

```bash
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit
```

### O que Faz

1. Verifica se há segredos
2. Bloqueia commit se encontrar
3. Exibe instruções para corrigir

### Exemplo de Saída

```
🔍 Scanning for secrets before commit...
✅ No secrets detected. Proceeding with commit.
```

ou

```
❌ SECRETS DETECTED! Commit aborted.

{
  "results": {
    "src/config.py": [
      {"type": "Hex High Entropy String", "secret": "sk_live_abc123"}
    ]
  }
}
```

---

## GitHub Actions Workflows

### secrets-scan.yml

Workflow que executa em cada push e pull request.

#### Etapas

1. **Secret Detection** - detect-secrets scan
2. **AWS Credentials Check** - Procura por padrões AWS
3. **GitHub Tokens Check** - Procura por tokens GitHub
4. **SAST Scan** - Bandit para código Python
5. **Dependency Check** - Safety para verificar CVEs

#### Visualizar Resultados

1. Vá para a aba **Actions**
2. Clique no workflow mais recente
3. Veja os logs por etapa

#### Falhas Comuns

| Problema | Causa | Solução |
|----------|-------|---------|
| Secret Detection Failed | Segredo encontrado | Remove o segredo, usa env var |
| AWS Credentials Found | Pattern AKIA encontrado | Não commite credentials AWS |
| GitHub Token Found | Pattern ghp_ encontrado | Revoke o token e cria novo |

---

## Boas Práticas

### 1. Nunca Commita Segredos

❌ ERRADO:
```python
database_password = "my_secure_password_123"
api_key = "sk_live_production_key"
```

✅ CORRETO:
```python
database_password = os.environ.get("DATABASE_PASSWORD")
api_key = os.environ.get("SATELLITE_API_KEY")
```

### 2. Use .env.example, Não .env

- `.env.example` → SIM, commita (sem valores reais)
- `.env` → NÃO, adiciona a .gitignore

```bash
# .gitignore
.env
.env.local
.env.*.local
*.pem
*.key
```

### 3. Rotação de Secrets

Periodicamente atualize os secrets:

```bash
# GitHub UI:
Settings → Secrets and variables → Actions → Update Secret
```

### 4. Auditoria de Acessos

Verifique quem acessou secrets:

```bash
# GitHub UI:
Settings → Security log
```

### 5. Comunicação Segura

Para compartilhar secrets com teammates:
- ✅ Use GitHub Secrets (encrypted)
- ✅ Use Vault ou gerenciador de secrets
- ❌ NUNCA via email ou Slack
- ❌ NUNCA em comentários ou issues

---

## Ciclo de Vida Seguro de Secrets

```
1. GERAÇÃO
   └─ Criar em local seguro (não no Git)

2. ARMAZENAMENTO
   └─ GitHub Secrets (encrypted at rest)

3. USO
   └─ Via os.environ.get() ou GitHub Actions env

4. ROTAÇÃO
   └─ Atualizar periodicamente (30-90 dias)

5. REVOGAÇÃO
   └─ Se comprometido, revogar imediatamente
```

---

## Resposta a Incidentes

### Cenário: Secret Commitado Acidentalmente

#### Passo 1: Identifique o Secret
```bash
# Ver histórico
git log --all -p | grep "secret_value"
```

#### Passo 2: Revogue o Secret
```bash
# Na plataforma original (AWS, GitHub, etc)
# Desative o key/token imediatamente
```

#### Passo 3: Remova do Git
```bash
# Remover do histórico (use git-filter-repo)
git filter-repo --invert-paths --path src/config.py  # Remove o arquivo
# OU
git filter-repo --replace-text replacements.txt  # Substitui a string
```

#### Passo 4: Force Push
```bash
git push --force-with-lease origin main
```

#### Passo 5: Crie um Secret Novo
```bash
# GitHub UI: Settings → Secrets → New secret
# Use novo valor em os.environ.get()
```

### Checklist pós-incidente

- [ ] Secret revogado na plataforma original
- [ ] Removido do git history
- [ ] Force push executado
- [ ] Novo secret gerado e configurado
- [ ] Logs auditados para acessos não autorizados
- [ ] Equipe notificada
- [ ] Documentação atualizada

---

## Manutenção Contínua

### Semanal

- [ ] Revisar logs de GitHub Actions
- [ ] Verificar se workflows passaram
- [ ] Monitorar alertas de segurança

### Mensal

- [ ] Atualizar dependências Python
- [ ] Revisar GitHub Secrets configurados
- [ ] Auditar acessos ao repositório

### Trimestral

- [ ] Rotacionar secrets críticos
- [ ] Revisar políticas de segurança
- [ ] Atualizar documentação de segurança
- [ ] Teste de resposta a incidentes

---

## Recursos Adicionais

- **[detect-secrets Documentation](https://detect-secrets.readthedocs.io/)**
- **[Bandit Documentation](https://bandit.readthedocs.io/)**
- **[GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)**
- **[OWASP Top 10](https://owasp.org/www-project-top-ten/)**
- **[CWE Top 25](https://cwe.mitre.org/top25/)**

---

## Contato e Suporte

Para reportar vulnerabilidades de segurança:
1. **NÃO** abra issues públicas
2. Use **Settings → Security → Report a vulnerability**
3. Forneça detalhes e reprodução

---

<div align="center">

**Segurança não é um produto, é um processo! 🔐**

Última atualização: 2026

</div>
