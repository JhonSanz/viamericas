# Data por defecto

Para poblar la información en la base de datos creé un archivo `seed.py` el cual se corre en la fase de construcción del docker compose por medio del comando personalizado `python manage.py populate`. Aqui se crearán dos usuarios con diferentes niveles de permisos

| username        | password          |
| --------------- | ----------------- |
| viamericas      | holamundo123      |
| restricted_user | restrictedpass123 |

esto es útil para evidenciar el manejo de permisos en el panel administrativo de django.

Adicionalmente se crearon datos para el resto de modelos, ya que la API solo fue creada para gestionar Event y Reservation.

# Personalizaciones para en panel administrativo

Adjuntaré algunos pantallazos para hacer mas facil la explicación

![image_0](image_0.png)
![image_1](image_1.png)

1. Modificación de estilos para la barra superior
2. Recuadro con eventos que se llevarán a cabo la proxima semana
3. PieChart con la información de número de eventos por categoría
4. Filtro avanzado por periodos de tiempo
5. Filtro avanzado incrustado en la plantilla de filtro por fecha específica en el calendario
6. Campo calculado adicional de total de reservas de cada evento

# Link para documentación con postman

- https://www.postman.com/dark-space-466960/viamericas/collection/f0faznp/viamericas

# Export de archivo xlsx

Para probar esta característica recomiendo utilizar el navegador web, no encontré como hacer que postamn procesara la respuesta para descargar el archivo. El queryparam puede ser event o category

- http://localhost:8000/report?model=event

# Correr localmente

1. `docker build -t my-django-app .`
2. `docker run -it --rm -p 8000:8000 my-django-app`
3. disfrutar

# Despliegue en AWS

0. Tener instalado `aws cli`
1. Tener configurado `aws config`
2. Entrar al directorio `/iac`
3. Activar el entorno virtual `.venv\Scripts\activate` o `.venv/bin/activate`
4. Ejecutar `pip install -r requirements.txt`
5. Ejectuar `cdk bootstrap`
6. Opcional `cdk synth` para ver la plantilla de cloud formation
7. Ejectuar `cdk deploy` para desplegar el contenido
8. Disfrutar
9. Recomendado `cdk destroy` para eliminar el stack

Como puede verse en el archivo `iac/iac_stack.py` la imagen de docker fue previamente subida a un repositorio y no se hizo ese step en el archivo de AWS CDK.

### 👇🚨🚨⚠️⚠️ IMPORTANTE ⚠️⚠️🚨🚨👇

> Este stack creará todos los recursos en AWS. Es importante recalcar que solamnete se creará el loadbalancer así que utilizaremos su DNS como URL para acceder a los servicios. Entonces, hay que buscar el balanceador en EC2 y copiar el DNS en postman o el software preferido para hacer peticiones.


# Diagrama de base de datos

![database](database.png)