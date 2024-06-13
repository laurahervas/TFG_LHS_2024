[GENERATIVE] Projecte per a interactuar amb els models de IA generativa

Aquest projecte publica una serie d'APIs per a que es pugui interactuar amb els models de IA generativa i recupera la informació cridant a les APIs del projecte [FASTAPI].

## Requisits

- Python (versió 3.12)
- Dependències del projecte instal·lades
- Anaconda o entorn virtual dedicat
- MongoDB

## Instal·lació de les dependències

Pots instal·lar les dependències amb les següents commandes:

#### Shell

```shell
python -m pip install --upgrade pip
```

```shell
pip install -r requirements.txt
```

#### Entorn virtual sense anaconda

```shell
pip install virtualenv
```

```shell
virtualenv vapi      
```

```shell
source vapi/bin/activate   
```

```shell
pip install -r requirements.txt
```

#### Entorn virtual amb anaconda

```shell
conda create env-api
```

```shell
conda activate env-api
```

```shell
pip install -r requirements.txt
```

## Configuració

El projecte utilitza les variables d'entorn emmagatzemades al fitxer `.env.{entorn}` on {entorn} en local es `dev`.

## Execució

```shell
uvicorn main:app --port 8001 --reload
```

## Exemples d'execució

### Generate

post http://127.0.0.1:8001/generative/generate
{
 "query": "que cuota anual tiene una tarjeta de debito",
  "cognitiveId": "1234567890",
  "userId": "myfirstuser"
}