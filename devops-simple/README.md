# Projet DevOps — Conteneurisation M2
# Timéo Locqueneux - Titouan Bodin - Pierre-Jean Le Rossignol - Sacha Vandemeulebroucke

Application web permettant de générer un QR code qui renvoie vers cet url, conteneurisée avec API, worker batch et reverse proxy.

# Architecture
```
Internet → Proxy (port 8080) → API (port 5000)
                             → Frontend (port 8080)
                             → Worker (batch, one-shot)
```

Les services communiquent sur un réseau interne `backend`. Seul le proxy est exposé.

# Composants

| Composant | Image de base | Rôle |
|-----------|--------------|------|
| **API** | `python:3.11-slim` | Expose `GET /welcome` et `GET /health` |
| **Proxy** | `nginx:1.25-alpine` | Reverse proxy vers l'API |
| **Frontend** | `nginx:1.27-alpine` |
| **Worker** | `python:3.11-alpine` | Tâche batch, s'exécute et se termine |


# Prérequis pour tester localement :
Docker Desktop installé et lancé.
```powershell
# 1. Copier la config
copy .env.example .env
# 2. Builder et lancer
docker compose up --build
# 3. Vérifier
docker compose ps
```

# L'application est disponible à cette adresse:
http://localhost:8080
# Tester les endpoints de l'API à ces adresses:
http://localhost:8080/welcome
http://localhost:8080/health

# Le test d'intégration (CI) se fait avec ce fichier:
tests/integration_test.py

# Les variables d'environnement
Fichier `.env` (copié depuis `.env.example`)

## Sécurité
Toutes les images utilisent **un utilisateur non-root** (uid 1000).
- L'API et le proxy ont un **HEALTHCHECK** actif
- Les services `api` et `worker` ne sont **pas exposés directement** — seul le proxy l'est
- Les deux réseaux Docker (`frontend` / `backend`) isolent les flux

## CI/CD
Le pipeline `.github/workflows/ci-cd.yml` :
1. **Build** les 3 images en parallèle
2. **Push** vers GitHub Container Registry
3. **Lance** les tests d'intégration

## Versioning
Les images sont taguées avec la version du tag Git (`v1.0.0`) et le SHA du commit :
```
ghcr.io/username/devops-project-api:1.0.0
ghcr.io/username/devops-project-api:sha-a1b2c3d
```
