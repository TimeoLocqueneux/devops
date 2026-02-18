# Projet DevOps — Conteneurisation M2

Application web conteneurisée avec API, worker batch et reverse proxy.

## Architecture

```
Internet → Proxy (port 8080) → API (port 5000)
                             → Worker (batch, one-shot)
```

Les services communiquent sur un réseau interne `backend`. Seul le proxy est exposé.

## Composants

| Composant | Image de base | Rôle |
|-----------|--------------|------|
| **API** | `python:3.11-slim` | Expose `GET /` et `GET /health` |
| **Proxy** | `nginx:1.25-alpine` | Reverse proxy vers l'API |
| **Worker** | `python:3.11-alpine` | Tâche batch, s'exécute et se termine |

## Démarrage rapide

**Prérequis** : Docker Desktop installé et démarré.

```bash
# 1. Copier la config
copy .env.example .env

# 2. Builder et lancer
docker compose build
docker compose up -d

# 3. Vérifier
docker compose ps
```

L'API est disponible sur **http://localhost:8080**

```bash
# Tester les endpoints
curl http://localhost:8080/
curl http://localhost:8080/health
```

## Commandes utiles

```bash
# Voir les logs
docker compose logs -f

# Voir les logs d'un service
docker compose logs api
docker compose logs worker

# Relancer le worker
docker compose up worker

# Arrêter
docker compose down

# Arrêter + supprimer les volumes
docker compose down -v
```

## Tests

```bash
# Tests d'intégration (stack doit être démarrée)
python tests/integration_test.py
```

## Variables d'environnement

Fichier `.env` (copié depuis `.env.example`) :

| Variable | Défaut | Description |
|----------|--------|-------------|
| `APP_VERSION` | `1.0.0` | Version affichée par l'API |
| `PROXY_PORT` | `8080` | Port exposé du proxy |

## Sécurité

Toutes les images utilisent **un utilisateur non-root** (uid 1000).

- L'API et le proxy ont un **HEALTHCHECK** actif
- Les services `api` et `worker` ne sont **pas exposés directement** — seul le proxy l'est
- Les deux réseaux Docker (`frontend` / `backend`) isolent les flux

### Scan de vulnérabilités (en local)

Installer [Trivy](https://aquasecurity.github.io/trivy/latest/getting-started/installation/) puis :

```bash
trivy image devops-api:1.0.0
trivy image devops-proxy:1.0.0
trivy image devops-worker:1.0.0
```

### Générer un SBOM (en local)

```bash
trivy image --format cyclonedx devops-api:1.0.0 > sbom-api.json
```

## CI/CD

Le pipeline `.github/workflows/ci-cd.yml` :

1. **Build** les 3 images en parallèle
2. **Push** vers GitHub Container Registry (tags : version sémantique + SHA du commit)
3. **Scan** chaque image avec Trivy (CRITICAL et HIGH)
4. **Génère** un SBOM CycloneDX sauvegardé 90 jours
5. **Lance** les tests d'intégration

## Versioning

Les images sont taguées avec la version du tag Git (`v1.0.0`) et le SHA du commit :

```
ghcr.io/username/devops-project-api:1.0.0
ghcr.io/username/devops-project-api:sha-a1b2c3d
```

## Politique de sécurité supply chain

| Sévérité | Délai de correction |
|----------|-------------------|
| CRITICAL | 24 h |
| HIGH | 7 jours |
| MEDIUM | 30 jours |
| LOW | 90 jours ou risque accepté |

Les vulnérabilités sont détectées à chaque build CI. Si une CVE CRITICAL est détectée, le build est marqué comme instable et l'équipe est notifiée.

## Structure du projet

```
devops-project/
├── api/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── proxy/
│   ├── Dockerfile
│   └── nginx.conf
├── worker/
│   ├── Dockerfile
│   └── worker.py
├── tests/
│   ├── structure-test.yaml
│   └── integration_test.py
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── docker-compose.yml
├── .env.example
├── .dockerignore
└── README.md
```
