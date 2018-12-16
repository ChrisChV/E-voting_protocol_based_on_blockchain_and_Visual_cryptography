# E-voting protocol based on Blockchain and Visual Cryptography

Implementación de Tesis de pregrado para votación electrónica remota.

## Configuración

* En el archivo src/Conf/serverHost colocar la información de las máquinas que van a ser nodo de Sufragio-Comisionados:

```
<usuarioMáquina1> <ip> <password> <groupId>
<usuarioMáquina1> <ip> <password> <groupId>
<usuarioMáquina1> <ip> <password> <groupId>
<usuarioMáquina1> <ip> <password> <groupId>
```
* En el archivo src/Conf/port colocar el puerto por el cual los servidores escucharan mensajes.
* En el archivo src/Conf/port colocar el líder de grupo inicial para cada máquina (Colocar la ip).
* En el archivo src/Conf/candidates colocar el nombre de cada candidato con su respectiva id:

```
<NombreCandidato1> <id>
<NombreCandidato2> <id>
<NombreCandidato2> <id>
```
## Despliegue y ejecución

* Inicie todas las máquinas que se encuentran en el archivo src/Conf/serverHost.
* Asegúrece de que las máquinas tengan comunicación ne red.
* Ejecutar el programa src/runConfigureServers. El programa copiará los archivos necesarios y configurará los servidores con la configuración especificada anteriormente.
* Iniciar el programa src/Blockchain/testServer.py con python en todos los servidores. Esto inicia el servidor en las máquinas y los deja a la espera de nuevos votos.
* Para enviar nuevos votos ejecute el programa src/runNewVote con los siguientes argumentos:

```
$> runNewVote <numOfVotes>
```
* Autamáticamente se crearán y se cifrarán votos para luego enviarlos a uno de los servidores.
* Disfrutar del espectáculo.
* Nota: si desea reiniciar el blockchain en todos los servidores, ejecutar el programa src/runResetServerBlockchain

## Video

Explicación del código, la configuración y ejecución de algunas pruebas:

https://www.youtube.com/watch?v=axks5RftIs4

