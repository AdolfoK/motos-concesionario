# Guía de despliegue en la nube (paso a paso, desde cero)

Esta guía despliega la plataforma en una arquitectura **multi-cloud real**:

- **AWS** → cómputo: una instancia **EC2** que ejecuta los contenedores
  (frontend nginx + backend Django) con `docker-compose`.
- **Azure** → datos: **Azure Database for PostgreSQL** + **Azure Blob Storage**
  para las imágenes de las motos.
- **Terraform** → toda la infraestructura como código (IaC).

```
   Internet
      │  HTTP (80)
      ▼
 ┌─────────────────────┐         ┌──────────────────────────┐
 │  AWS · EC2 (Ubuntu) │  SSL    │  Azure                   │
 │  ┌───────────────┐  │ ──────► │  PostgreSQL Flexible     │
 │  │ nginx (front) │  │         │  (base de datos)         │
 │  │ Django (back) │  │ ──────► │  Blob Storage (imágenes) │
 │  └───────────────┘  │         └──────────────────────────┘
 └─────────────────────┘
```

> ⚠️ **Costos.** AWS EC2 `t3.micro` es elegible para la capa gratuita (Free
> Tier) el primer año. Azure PostgreSQL Burstable B1ms cuesta ~12-15 USD/mes,
> cubierto por el crédito de Azure for Students. **Al terminar, ejecuta el
> teardown (Paso 8) para no gastar de más.**

---

## Paso 0 — Requisitos (ya instalados)

Ya instalamos en tu equipo:

- AWS CLI, Azure CLI y Terraform.

Verifica en una terminal **nueva** de PowerShell:

```powershell
aws --version
az version
terraform version
```

Si algún comando no se reconoce, cierra y abre PowerShell de nuevo (el PATH se
actualizó tras instalar).

---

## Paso 1 — Generar tu clave SSH

Sirve para entrar a la instancia EC2. En PowerShell:

```powershell
ssh-keygen -t rsa -b 4096 -f "$env:USERPROFILE\.ssh\id_rsa" -N '""'
```

Esto crea dos archivos:

- `id_rsa` → clave **privada** (NO la compartas).
- `id_rsa.pub` → clave **pública** (la pondremos en Terraform).

Muestra la pública (la copiarás más adelante):

```powershell
Get-Content "$env:USERPROFILE\.ssh\id_rsa.pub"
```

---

## Paso 2 — Crear las cuentas

### Azure for Students
1. Entra a https://azure.microsoft.com/es-es/free/students
2. Inicia sesión con tu correo institucional (o verifica tu condición de
   estudiante). Obtienes **100 USD de crédito sin tarjeta**.
   - *Si no tienes correo institucional:* usa la cuenta gratuita normal
     (https://azure.microsoft.com/free) — da 200 USD por 30 días pero pide
     tarjeta (no se cobra si no superas el crédito).

### AWS
1. Entra a https://aws.amazon.com → "Crear una cuenta de AWS".
2. Necesitas correo, tarjeta (no se cobra dentro del Free Tier) y teléfono.
3. Tras crearla, crea un **usuario IAM** para no usar la cuenta raíz:
   - Consola AWS → busca **IAM** → *Users* → *Create user*.
   - Nombre: `terraform`. Marca *Provide user access to the AWS Management
     Console* solo si quieres; lo importante es el acceso programático.
   - *Set permissions* → *Attach policies directly* → marca
     **AdministratorAccess** (suficiente para esta práctica).
   - Crea el usuario. Entra a él → pestaña *Security credentials* →
     *Create access key* → tipo *Command Line Interface (CLI)*.
   - Guarda el **Access key ID** y el **Secret access key** (solo se muestran
     una vez).

   > ⚠️ **Importante:** el usuario IAM **debe** tener la política
   > **AdministratorAccess** adjunta, o Terraform fallará con
   > `UnauthorizedOperation`. Verifícalo en *Permissions* → *Add permissions*
   > → *Attach policies directly* → `AdministratorAccess`.

---

## Paso 3 — Autenticar las CLIs

### Azure
```powershell
az login
```
Se abre el navegador. Inicia sesión. Al volver, verifica la suscripción:
```powershell
az account show
```

### AWS
```powershell
aws configure
```
Pega cuando te pida:
- **AWS Access Key ID**: el del usuario IAM.
- **AWS Secret Access Key**: el del usuario IAM.
- **Default region name**: `us-east-1`
- **Default output format**: `json`

Verifica:
```powershell
aws sts get-caller-identity
```

---

## Paso 4 — Desplegar la capa de datos en Azure

```powershell
cd "C:\Users\AdolfoK\Desktop\Concesionaria motos\infra\azure"

# 1) Crea tu archivo de variables a partir del ejemplo
Copy-Item terraform.tfvars.example terraform.tfvars
notepad terraform.tfvars   # define db_admin_password (8+ con mayús/minús/números)

# 2) Inicializa Terraform (descarga el proveedor de Azure)
terraform init

# 3) Revisa lo que se va a crear
terraform plan

# 4) Aplica (escribe 'yes' para confirmar)
terraform apply
```

Tarda ~5-10 min (PostgreSQL gestionado demora). Al terminar verás los outputs
(`pg_fqdn`, `storage_account_name`, etc.). **No borres la carpeta**: el estado
(`terraform.tfstate`) lo lee la capa de AWS.

> ⚠️ **Regiones restringidas en Azure for Students.** Las suscripciones de
> estudiante limitan las regiones por política y, además, PostgreSQL está
> *offer-restricted* en varias (ej: `eastus`, `eastus2` fallan con
> `LocationIsOfferRestricted`). Por eso el PostgreSQL se despliega por defecto
> en **`brazilsouth`** (`var.pg_location`), permitida y cercana a Chile.
> Para ver QUÉ regiones permite tu suscripción:
> ```powershell
> az policy assignment list --query "[].parameters" -o json
> ```
> Busca `listOfAllowedLocations`. Si `brazilsouth` no estuviera, cambia
> `pg_location` a una de las permitidas (ej: `chilecentral`, `mexicocentral`).

> 🔐 Anota la `db_admin_password` que usaste: la necesitas idéntica en AWS.

---

## Paso 5 — Subir el proyecto a GitHub (ya hecho)

La instancia EC2 **clona tu repositorio** para construir las imágenes, así que
el código debe estar en GitHub (rama `main`) y el repo debe ser **público**
(o configurar un token). Ya está publicado en:
`https://github.com/AdolfoK/motos-concesionario`

Si haces cambios, recuerda `git push` antes de desplegar AWS.

---

## Paso 6 — Desplegar la capa de cómputo en AWS

```powershell
cd "C:\Users\AdolfoK\Desktop\Concesionaria motos\infra\aws"

Copy-Item terraform.tfvars.example terraform.tfvars
notepad terraform.tfvars
```

Completa en `terraform.tfvars`:
- `ssh_public_key`  → pega el contenido de `id_rsa.pub` (Paso 1).
- `my_ip_cidr`      → tu IP pública + `/32`. Obténla con:
  ```powershell
  (Invoke-RestMethod https://ifconfig.me/ip) + "/32"
  ```
- `db_admin_password` → **la misma** que en Azure.
- `django_secret_key` → una cadena larga aleatoria. Puedes generarla con:
  ```powershell
  -join ((48..57)+(65..90)+(97..122) | Get-Random -Count 50 | ForEach-Object {[char]$_})
  ```
- `whatsapp_numero` → el número de la concesionaria.

Luego:
```powershell
terraform init
terraform plan
terraform apply       # escribe 'yes'
```

Al terminar verás:
```
app_url     = "http://X.X.X.X"
public_ip   = "X.X.X.X"
ssh_command = "ssh ubuntu@X.X.X.X"
```

La instancia tarda **3-6 minutos** adicionales en arrancar: instala Docker,
clona el repo, construye las imágenes y levanta los contenedores.

---

## Paso 7 — Verificar

1. Abre `http://<public_ip>` en el navegador → deberías ver el catálogo.
2. Prueba el módulo de **Reservar hora** → genera el enlace de WhatsApp.
3. Entra como admin (`/login`, admin / tu contraseña) y sube una imagen:
   se almacena en **Azure Blob Storage**.

### Si no carga, conéctate por SSH y revisa los logs:
```powershell
ssh ubuntu@<public_ip>
# dentro de la instancia:
sudo cat /var/log/user-data.log        # log del arranque
cd /opt/app
sudo docker compose -f docker-compose.cloud.yml ps
sudo docker compose -f docker-compose.cloud.yml logs backend --tail 50
```

Errores comunes:
- **Backend no conecta a la DB** → revisa que `db_admin_password` sea idéntica
  en Azure y AWS, y que la regla de firewall de PostgreSQL permita la IP.
- **Build se queda sin memoria** → ya añadimos 2 GB de swap; si persiste, sube
  a `instance_type = "t3.small"`.

---

## Paso 8 — Apagar todo (teardown) para no gastar

**Importante al terminar la evaluación.** Destruye en orden inverso:

```powershell
cd "C:\Users\AdolfoK\Desktop\Concesionaria motos\infra\aws"
terraform destroy     # escribe 'yes'

cd "..\azure"
terraform destroy     # escribe 'yes'
```

Esto elimina la instancia, la IP, la base de datos y el almacenamiento.

---

## (Opcional) DevSecOps — CI/CD con Trivy

El repo incluye `.github/workflows/ci.yml`, que en cada `push` a `main`:
1. Construye las imágenes Docker de frontend y backend.
2. Las escanea con **Aqua Trivy** (falla si hay vulnerabilidades CRÍTICAS).
3. Corre `manage.py check` del backend.

Se ejecuta automáticamente en GitHub (pestaña **Actions**) sin configuración
adicional.

---

## Resumen de comandos

| Acción | Carpeta | Comando |
|--------|---------|---------|
| Crear datos (Azure) | `infra/azure` | `terraform init && terraform apply` |
| Crear cómputo (AWS) | `infra/aws` | `terraform init && terraform apply` |
| Ver la app | navegador | `http://<public_ip>` |
| Apagar AWS | `infra/aws` | `terraform destroy` |
| Apagar Azure | `infra/azure` | `terraform destroy` |
