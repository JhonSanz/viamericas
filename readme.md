# Link para documentación con postman

- https://www.postman.com/dark-space-466960/viamericas/collection/f0faznp/viamericas

# Export de archivo xlsx



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