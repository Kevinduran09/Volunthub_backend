# Volunthub Backend v2 - Repo gaps y mejoras

Este documento resume faltantes y refactors recomendados. Se organiza por categoria y prioriza impacto tecnico y operabilidad.

## 1) Modelo de datos y dominio
- Falta relacion real entre eventos y categoria/creador. Hoy `EventModel` no tiene `category_id` ni `created_by_user_id`, por lo que `get_by_category` no filtra y `EventType.category/created_by` no puede resolver datos reales.
- `TaskModel.event` usa `Mapped[List["EventModel"]]` pero es relacion many-to-one; deberia ser un solo `EventModel`.
- `InscriptionModel` no tiene `registered_at`; GraphQL expone `registered_at` como campo obligatorio.
- `EventRepository.get_by_category` retorna todos los eventos (stub), no filtra por categoria.

## 2) GraphQL schema y resolvers
- Campos y nombres mezclados ES/EN en schema y mappers; estandarizar nombres y mappings.
- `UserStats` usa campos en espanol; definir version en ingles o unificar naming.
- Algunos fields en GraphQL son obligatorios pero el modelo permite `NULL` (ej. `TaskType` y `ParticipantType`).
- Resolver de conteos usa N+1 (loop con `get_event_participants_count` por evento). Migrar a DataLoader o query agregada.
- `app/api/routes.py` esta vacio: decidir si se elimina o se habilita REST complementario.

## 3) Servicios y repositorios
- `BaseRepository.update` tiene firma `entity` pero implementaciones usan `dict`; alinear firma y contrato.
- `UserRepository.get_all` usa `UserModel.id.desc` sin ejecutar `desc()`.
- `UserRepository.search` usa `like = f"%{criterio.strip()}"` (falta `%` al final), podria no encontrar coincidencias parciales.
- `InscriptionRepository.count_by_event_id` usa `len(list(...))` en vez de `COUNT(*)`.
- `EventService.create_event` usa status `pendint` (typo).
- `UserRepository.get_by_email` hace `print(result)`; usar logging estructurado.

## 4) Autenticacion y autorizacion
- No hay autenticacion real ni extraccion de `user_id` en `GraphQLContext`.
- Mutations usan `request.user_id` o `request.state.user_id`, pero no hay middleware que lo setee.
- Falta estrategia de autorizacion (roles, owner checks, permisos por evento).

## 5) Observabilidad y logging
- `GraphQLContext` crea `logger = object()`; no hay logger real.
- Falta configuracion de logging central (niveles, formato, request id, user id).
- No hay trazas para SQL o GraphQL (latencias, errores, query timing).

### Estrategia sugerida de logging
- Configurar `structlog` o `logging` nativo con JSON.
- Agregar middleware para `request_id` y `user_id`.
- Loggear errores GraphQL y timings (resolver time + total request time).

## 6) Suscripciones con Redis
- No hay soporte de subscriptions (GraphQL real-time) ni infraestructura para pub/sub.
- Strawberry soporta subscriptions, pero falta transporte y backend.

### Estrategia sugerida con Redis
- Usar Redis Pub/Sub como bus de eventos.
- Emisor: en mutations (`createEvent`, `inscribirse`) publicar eventos.
- Consumidor: resolver de subscription escucha canal Redis y emite a clientes.
- Agregar workers o background task para conectar Redis.

## 7) Imagenes y media
- Solo existe `image_url`, no hay pipeline de upload/validacion.
- Falta definir storage (S3, GCS, local, Supabase) y estrategia de signed URLs.
- No hay validacion de formatos, tamanos ni optimizacion (thumbnails).

### Estrategia sugerida para imagenes
- Crear endpoint de upload (REST o GraphQL mutation) que guarde en storage.
- Generar URL publica/signed y persistir en `image_url`.
- Agregar validacion de tamano y tipo MIME.

## 8) Infra y configuracion
- Duplicidad entre `settings.py` y `db_settings.py` (DB_PASS vs DB_PASSWORD).
- `db-compose.yml` usa `POSTGRES_PASS`, pero settings esperan `DB_PASS`/`DB_PASSWORD`.
- `README.md` vacio; falta guia de setup, migraciones y ejecucion.
- `.gitignore` ignora `poetry-lock` pero el archivo real es `poetry.lock`.

## 9) Performance
- N+1 en conteos, tareas y resolvers anidados; agregar DataLoader o joins agregados.
- Falta `GIST` index para `events.location` (mencionado en downgrade pero no creado en upgrade).
- `search` usa `ILIKE` sin indices de texto; evaluar `GIN`/`tsvector`.

## 10) Testing y calidad
- No hay tests; agregar smoke tests para GraphQL (queries y mutations).
- No hay CI; agregar workflow basico para lint/test.
- `ruff/black/mypy` no estan configurados con reglas y no hay pre-commit.

## 11) Documentacion y DX
- `README.md` vacio; agregar:
  - setup local
  - variables de entorno
  - migraciones (alembic)
  - run con uvicorn
  - ejemplos de queries

## 12) Seguridad
- Falta configuracion CORS en FastAPI.
- No hay rate limit ni protecciones basicas en GraphQL.
- No hay validacion de input para tamano max en strings.

## 13) Migrations
- Schema inicial no crea index `idx_events_location` pero lo elimina en downgrade.
- Si se agregan relaciones nuevas, falta migracion y backfill.

---

## Roadmap sugerido (orden recomendado)
1) Autenticacion + middleware (para user_id en contexto).
2) Logging estructurado + request tracing.
3) Eliminar N+1 con DataLoader (conteos, tareas, categoria, created_by).
4) Normalizar naming y mappers (ES/EN).
5) Completar relaciones en modelo y repo (category, created_by).
6) Suscripciones con Redis.
7) Pipeline de imagenes.
8) Tests + CI.
