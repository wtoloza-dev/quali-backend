# Production Database Access

## Architecture

PostgreSQL runs inside Docker Swarm on the `dokploy-network` overlay network. The host cannot reach container IPs directly, so a **socat proxy container** bridges the connection.

```
DBeaver → SSH Tunnel → host:5433 → quali-db-proxy (socat) → quali-postgre-xathga:5432
```

## Containers

| Container | Purpose | Notes |
|-----------|---------|-------|
| `quali-postgre-xathga` | Quali app DB (PostgreSQL 18) | On `dokploy-network`, no published ports |
| `quali-db-proxy` | socat TCP proxy | Bridges `host:5433` → `quali-postgre-xathga:5432` |
| `dokploy-postgres` | Dokploy internal DB | Do not touch |

## Proxy Service

`quali-db-proxy` is a Docker Swarm service (not managed by Dokploy). It auto-restarts on crash/reboot.

### Creation command

```bash
docker service create \
  --name quali-db-proxy \
  --network dokploy-network \
  --publish published=5433,target=5433,mode=host \
  --constraint 'node.role==manager' \
  alpine/socat \
  TCP-LISTEN:5433,fork,reuseaddr TCP:quali-postgre-xathga:5432
```

### Management

```bash
# Check status
docker service ls | grep quali-db-proxy

# Restart
docker service update --force quali-db-proxy

# Remove (if needed)
docker service rm quali-db-proxy
```

## DBeaver Connection

### 1. SSH Tab (click + → SSH)

| Field | Value |
|-------|-------|
| Host/IP | `46.225.71.170` |
| Port | `22` |
| User name | `root` |
| Authentication | Public Key |

### 2. Main Tab

| Field | Value |
|-------|-------|
| Host | `localhost` |
| Port | `5433` |
| Database | `quali_prod` |
| Username | `quali_prod` |
| Password | *(see Dokploy env vars)* |

## Security

- Port 5433 is bound to the host only (`mode=host`) — accessible via SSH tunnel
- No database ports are exposed to the public internet
- Access requires SSH key authentication to the server
- DB credentials are stored in Dokploy as environment variables on the `quali-postgre` service
