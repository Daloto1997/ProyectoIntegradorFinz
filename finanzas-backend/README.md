# 💰 Finanzas Backend — Spring Boot

Backend REST para gestión de finanzas personales con autenticación JWT.

## 🛠 Stack Tecnológico
- **Java 17** + **Spring Boot 3.2**
- **Spring Security** + **JWT (JJWT 0.11.5)**
- **Spring Data JPA** + **Hibernate**
- **PostgreSQL**
- **Lombok**
- **Maven**

---

## 🏗 Arquitectura del Proyecto

```
src/main/java/com/finanzas/
├── config/               # Configuración de seguridad y CORS
├── controller/           # Capa de presentación (REST endpoints)
├── dto/
│   ├── request/          # DTOs de entrada con validaciones
│   └── response/         # DTOs de salida
├── exception/            # Manejo global de excepciones
├── model/                # Entidades JPA
├── repository/           # Interfaces Spring Data JPA
├── security/             # JWT Filter y JwtService
└── service/
    ├── impl/             # Implementaciones de servicios
    └── *.java            # Interfaces de servicios
```

---

## ⚙️ Configuración

### Base de Datos PostgreSQL
```sql
CREATE DATABASE finanzas_db;
```

### `application.properties`
```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/finanzas_db
spring.datasource.username=postgres
spring.datasource.password=tu_password
app.jwt.secret=404E635266556A586E3272357538782F413F4428472B4B6250645367566B5970
app.jwt.expiration=86400000
```

---

## 🔐 Autenticación

Todos los endpoints (excepto `/auth/**`) requieren header:
```
Authorization: Bearer <token>
```

---

## 📡 Endpoints de la API

### Auth — `/api/auth`
| Método | Endpoint       | Descripción         |
|--------|----------------|---------------------|
| POST   | `/register`    | Registrar usuario   |
| POST   | `/login`       | Iniciar sesión      |

#### Registro
```json
POST /api/auth/register
{
  "nombre": "Juan Pérez",
  "email": "juan@email.com",
  "password": "seguro123"
}
```

#### Login
```json
POST /api/auth/login
{
  "email": "juan@email.com",
  "password": "seguro123"
}
```

---

### Cuentas — `/api/cuentas`
| Método | Endpoint  | Descripción              |
|--------|-----------|--------------------------|
| POST   | `/`       | Crear cuenta             |
| GET    | `/`       | Listar cuentas           |
| GET    | `/{id}`   | Obtener cuenta           |
| PUT    | `/{id}`   | Actualizar nombre        |
| DELETE | `/{id}`   | Eliminar cuenta          |

```json
POST /api/cuentas
{
  "nombre": "Cuenta Nómina",
  "saldoActual": 1500000.00
}
```

---

### Categorías — `/api/categorias`
| Método | Endpoint  | Descripción                            |
|--------|-----------|----------------------------------------|
| POST   | `/`       | Crear categoría                        |
| GET    | `/`       | Listar (filtrar con `?tipo=INGRESO`)   |
| GET    | `/{id}`   | Obtener categoría                      |
| PUT    | `/{id}`   | Actualizar                             |
| DELETE | `/{id}`   | Eliminar                               |

```json
POST /api/categorias
{
  "nombre": "Alimentación",
  "tipo": "GASTO",
  "color": "#FF5733"
}
```

---

### Transacciones — `/api/transacciones`
| Método | Endpoint  | Descripción                                         |
|--------|-----------|-----------------------------------------------------|
| POST   | `/`       | Registrar transacción (actualiza saldo automático)  |
| GET    | `/`       | Listar (filtrar con `?cuentaId=1` o `?categoriaId`) |
| GET    | `/{id}`   | Obtener transacción                                 |
| PUT    | `/{id}`   | Actualizar (revierte y aplica nuevo monto)          |
| DELETE | `/{id}`   | Eliminar (revierte el saldo)                        |

```json
POST /api/transacciones
{
  "cuentaId": 1,
  "categoriaId": 2,
  "monto": 50000.00,
  "tipo": "GASTO",
  "descripcion": "Mercado semanal"
}
```

---

### Metas — `/api/metas`
| Método | Endpoint        | Descripción            |
|--------|-----------------|------------------------|
| POST   | `/`             | Crear meta             |
| GET    | `/`             | Listar metas           |
| GET    | `/{id}`         | Obtener meta           |
| PATCH  | `/{id}/abonar`  | Abonar monto a la meta |
| DELETE | `/{id}`         | Eliminar meta          |

```json
PATCH /api/metas/1/abonar
{
  "monto": 200000.00
}
```

---

### Deudas — `/api/deudas`
| Método | Endpoint      | Descripción                            |
|--------|---------------|----------------------------------------|
| POST   | `/`           | Registrar deuda                        |
| GET    | `/`           | Listar (filtrar con `?tipo=POR_PAGAR`) |
| GET    | `/{id}`       | Obtener deuda                          |
| PATCH  | `/{id}/pago`  | Registrar pago parcial o total         |
| DELETE | `/{id}`       | Eliminar deuda                         |

```json
POST /api/deudas
{
  "personaEntidad": "Banco XYZ",
  "montoTotal": 5000000.00,
  "tipo": "POR_PAGAR",
  "fechaVencimiento": "2025-12-31"
}
```

---

### Resumen / Dashboard — `/api/resumen`
| Método | Endpoint | Descripción                                   |
|--------|----------|-----------------------------------------------|
| GET    | `/`      | Resumen mensual (filtrar con `?mes=1&anio=2025`) |

**Respuesta:**
```json
{
  "mes": 4,
  "anio": 2025,
  "totalIngresos": 5000000.00,
  "totalGastos": 1200000.00,
  "balance": 3800000.00,
  "totalCuentas": 2,
  "saldoTotalCuentas": 8500000.00,
  "metasActivas": 3,
  "deudasPendientes": 1
}
```

---

## 🔒 Reglas de Negocio Implementadas

- ✅ Cada usuario solo puede ver/modificar sus propios datos
- ✅ El saldo de la cuenta se actualiza automáticamente al crear/editar/eliminar transacciones
- ✅ Validación de saldo suficiente antes de registrar un GASTO
- ✅ El tipo de transacción debe coincidir con el tipo de la categoría
- ✅ El `montoPagado` de una deuda no puede superar el `montoTotal`
- ✅ No se pueden abonar metas ya completadas

---

## 🚀 Cómo ejecutar

```bash
# 1. Clonar y entrar al proyecto
cd finanzas-backend

# 2. Configurar base de datos en application.properties

# 3. Ejecutar
mvn spring-boot:run
```

La API estará disponible en: `http://localhost:8080/api`
