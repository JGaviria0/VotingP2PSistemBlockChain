# Sistema de votación con blockchain en una arquitectura p2p

Este proyecto esta desarrollado para la materia de Arquitectura cliente servidor de la Universidad Tecnológica de Pereira, el objetivo es poder hacer una votación usando una arquitectura p2p en anillo.

## Run Locally

Clone the project

```bash
  https://github.com/JGaviria0/VotingP2PSistemBlockChain.git
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

## .env
Configure the environment variables, copy and paste this variables in a new file with name **.env** in the root of the project. 

```bash
BUF_SIZE=1048576  
MAX_RANGE=4294967296 #2^32
RANDOM_CHARACTERS=20
PRINCIPAL_PATH='./../'

UPLOAD_TYPE='upload'
GET_UPLOAD_DATA_TYPE='getUploadData'
GET_DOWNLOAD_DATA_TYPE='getDownloadData'
DOWNLOAD_TYPE='download'
FIND_POSITION_TYPE='searchPos'
CONFIRM_SUSCRIPTION='confirmPos'
FILE_SAVED='saved'
LIST_TYPE='list'
SEND_TYPE='sending'
MAGNET_LINK='link'

MAIN_DIRECTORY='./Files/'
NODES_PORT=4000

#codes:
SUCCESS_CODE=202
SEND_FILE_CODE=200
FILE_ALREADY_EXITS_CODE=201
FILE_DOESNT_EXITS_CODE=404
DOWNLOAD_FILE_CODE=202
ASK_NEXT_ONE=209
ALL_GOOD=203
```

### Start the first node

```bash
  cd Node
  python3 main.py --firstNode -port [port number]
```
Change [port number] for any port you want. 

### Start the rest of the nodes

```bash
  cd Node
  python3 main.py -address [IP]:[port] -port [port number]
```
Change [IP] for the IP of the node you want to connect, if you only have one node (first node) use the IP of that node, the same for [port], example (**192.168.0.2:1234**).
Change [port number] for any port you want. 

### Run the client, open other terminal

- **Upload**
    ```bash
    python3 client.py --upload -address [IP]:[port] -fileName [file name]
    ```
Change [IP] for the IP of the node you want to connect, if you only have one node (first node) use the IP of that node, the same for [port], example (**192.168.0.2:1234**).
Change [file name] for the name of the file do you want to upload, **it have to be in the same folder of main.py**. 

- **Download**
    ```bash
    python3 client.py --download -address [IP]:[port] -magnetLink [magnet link]
    ```
Change [IP] for the IP of the node you want to connect, if you only have one node (first node) use the IP of that node, the same for [port], example (**192.168.0.2:1234**).
Change [magnet link] for the magnet link of your file, is looks like **7399ccd544529d1bf2dd74f7e0814bcbdee42fb536c872a0850aaffdc182775f**.

## Examples

- **Download**
    ```bash
    python3 client.py --download -address 192.168.1.12:1234 -magnetLink 7399ccd544529d1bf2dd74f7e0814bcbdee42fb536c872a0850aaffdc182775f
    ```

- **Upload**
    ```bash
    python3 client.py --upload -address 192.168.1.12:4321 -fileName Test.txt
    ```
