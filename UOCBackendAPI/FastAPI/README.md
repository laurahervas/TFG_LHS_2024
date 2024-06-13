# [FASTAPI] Projecte per a interactuar amb base de dades

Aquest projecte publica una serie d'APIs per a que es pugui gestionar la informació que s'emmagatzema a la base de dades com son embeddings, corpus i prompts. La base de dades escollida es MongoDB.

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

## Instal·lació de la Base de Dades

Descarrega e instal·la la base de dades:
https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x-tarball/

Arrenca la base de dades

```shell
#mongod --dbpath ~/Documents/Developer/MongoDB/data/db --logpath ~/Documents/Developer/MongoDB/data/log/mongodb/mongo.log --fork
mongod --dbpath /Users/laurahervas/Documents/Developer/MongoDB/data/db --logpath /Users/laurahervas/Documents/Developer/MongoDB/data/log/mongodb/mongo.log --fork
```

## Configuració

El projecte utilitza les variables d'entorn emmagatzemades al fitxer `.env.{entorn}` on {entorn} en local es `dev`.

## Execució

```shell
uvicorn main:app --port 8000 --reload
```

## Exemples d'execució

### Prompts

get http://127.0.0.1:8000/prompt/reload_prompts

get http://127.0.0.1:8000/prompt/code/{code} -> ejemplo code=1

get http://127.0.0.1:8000/prompt/{_id} -> ejemplo _id=6623d119585db4f4eb741ab5


### Corpus
get http://127.0.0.1:8000/corpus/reload_corpus

get http://127.0.0.1:8000/corpus/code/{code} -> ejemplo code=419915

get http://127.0.0.1:8000/corpus/{_id} -> ejemplo _id=6623a273394f039752896845

get http://127.0.0.1:8000/corpus/codelist/?listdocs=[{"code": 418183, "similarity": 0.8948}, {"code": 418606, "similarity": 0.8852}]

### Embeddings
get http://127.0.0.1:8000/embeddings/reload_empbeddings 

get http://127.0.0.1:8000/embeddings/ -> get all database embeddings

get http://127.0.0.1:8000/embeddings/search/?user_query='que cuota anual tiene una tarjeta de debito' -> get embedding from user_query

post http://127.0.0.1:8000/embeddings/
{
"code": 00000,
"embeddings": [
    -0.030527226626873016,
    0.002666973741725087,
    0.014002280309796333,
    0.012143595144152641,
],
 "motivo": ""
}
### Conversation
get http://127.0.0.1:8000/conversation/all
get http://127.0.0.1:8000/conversation/{id} -> ejemplo id=”6640be2cfe252944e0a753bd”
post http://127.0.0.1:8000/conversation/  
{
  "id": "6640be2cfe252944e0a753bd",
  "user": "662eac875a187ab12cafc923", 
  "conversation": [{
      "query": "que cuota anual tiene una tarjeta de debito",
    }]
}
delete http://127.0.0.1:8000/conversation/clean
put http://127.0.0.1:8000/conversation
{
  "id": "6640be2cfe252944e0a753bd",
  "user": "662eac875a187ab12cafc923", 
  "conversation": [{
      "query": "que cuota anual tiene una tarjeta de debito",
      "response": "bla bla bla”
    }]
}





