# Roadmap - MVP de Producción

Este documento define las funcionalidades necesarias para el **MVP en producción** del proyecto, con un **servidor funcional instalable mediante Docker Compose**.  
Además, incluye un apartado de **opciones futuras/premium** para evolucionar el sistema.

---

## ✅ MVP (necesario para un servidor funcional instalable)

- **Servicio Postgres** en Docker Compose con volumen persistente. _(Normal)_
- **Esquema inicial** (usuarios, licencias, jobs, archivos) con migraciones Alembic. _(Normal)_
- **API REST**: subir audio → job → transcripción → resultado en DB. _(Fácil)_
- **Listado de jobs** por usuario con estado y timestamps. _(Fácil)_
- **Detalle de job** con métricas básicas (duración audio, tiempo de proceso). _(Fácil)_
- **Descarga de transcript** en TXT/JSON. _(Fácil)_
- **Exportar SRT/VTT** desde segmentos. _(Fácil)_
- **Cola de procesamiento visible** (estado: encolado, en ejecución, terminado, error). _(Normal)_
- **Health checks** (API, worker, Redis, DB). _(Fácil)_
- **Imagen Docker con Compose** (api, worker, redis, db, reverse-proxy con HTTPS automático). _(Difícil)_
- **Variables de entorno** para configurar modelo, device, límites, `JWT_SECRET`, DB URL. _(Fácil)_
- **Documentación de instalación** en VPS (paso a paso). _(Fácil)_

---

## ⏩ Opcional / Futuro (premium o mejoras posteriores)

- **Gestión de usuarios con roles** (admin/usuario). _(Normal)_
- **Middleware de licencias** (validación firma + gating de features). _(Difícil)_
- **Rate limiting** por usuario/IP (jobs por día, tamaño máximo). _(Normal)_
- **Visor avanzado de segmentos en la UI** (timestamps y copia por párrafo). _(Normal)_
- **Reintentar job fallido y cancelar job en cola.** _(Normal)_
- **Búsqueda y filtros avanzados** (idioma, modelo, fecha). _(Fácil)_
- **Tema claro/oscuro y branding configurable** por env. _(Fácil)_
- **Métricas Prometheus en `/metrics`** (tiempos, colas, errores). _(Normal)_
- **Alertas simples**: flag en UI si el worker no procesa en N minutos. _(Normal)_
- **Soporte multi-idioma en UI.** _(Fácil)_
- **Integración con sistema de pagos/licencias externas.** _(Difícil)_
