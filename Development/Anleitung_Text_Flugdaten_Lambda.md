
# Anleitung: Test um mittels AWS Lambda und S3 Flugdaten von einer API zu speichern

Diese Anleitung beschreibt, wie man eine AWS Lambda-Funktion einrichtet, die Flugverspätungsdaten von der AeroDataBox API abruft und die Ergebnisse als JSON-Datei in einem S3 Bucket speichert.

## 1. S3 Bucket erstellen

1. Melde dich bei der AWS Management Console an.
2. Gehe zu **S3** und klicke auf **Bucket erstellen**.
3. Gib dem Bucket einen eindeutigen Namen (z.B. `datalakepartitiontwo`).
4. Wähle die Region, in der der Bucket erstellt werden soll.
5. Optional: Aktiviere **Verschlüsselung** oder **Versionierung** nach Bedarf.
6. Klicke auf **Bucket erstellen**.

## 2. Lambda Layers für Python erstellen

Lambda Layers ermöglichen es, externe Bibliotheken in deiner Lambda-Funktion zu verwenden.

Folge der Vorlesung (Session Recording) bei der Session "Data Ingestion".

Code:
https://gist.github.com/jose0628/377f7a24650844474155f8cddfb6f665

> Anmerkung: ChatGPT schlägt vor, dass man die zip-Datei lokal erstellt.

## 3. Lambda-Funktion erstellen

1. Gehe zu **Lambda** > **Funktion erstellen**.
2. Gib der Funktion einen Namen (z.B. `airport_delay_data_lambda`).
3. Wähle **Python 3.x** als Laufzeit.
4. Wähle eine bestehende Rolle.
5. Erstelle die Funktion.

## 4. Lambda-Code einfügen

Füge den folgenden Python-Code in die Lambda-Funktion ein und speichere ihn:

```python
import requests
import json
import boto3
from datetime import datetime

API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' # nicht öffentlich, André hat API
S3_BUCKET_NAME = 'datalakepartitiontwo'  # Dein S3-Bucket-Name

base_url = 'https://aerodatabox.p.rapidapi.com/airports'
code_type = 'iata'
airport_code = 'ZRH'

endpoint = f'/{code_type}/{airport_code}/delays'

headers = {
    'X-RapidAPI-Key': API_KEY,
    'X-RapidAPI-Host': 'aerodatabox.p.rapidapi.com'
}

s3 = boto3.client('s3')

def lambda_handler(event, context):
    response = requests.get(base_url + endpoint, headers=headers)

    if response.status_code == 200:
        airport_delay_data = response.json()
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f'airport_delays_zrh_{current_time}.json'
        json_data = json.dumps(airport_delay_data)

        try:
            s3.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=file_name,
                Body=json_data,
                ContentType='application/json'
            )
            return {
                'statusCode': 200,
                'body': f'Successfully uploaded {file_name} to S3 bucket {S3_BUCKET_NAME}'
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': f"Error uploading to S3: {str(e)}"
            }

    else:
        return {
            'statusCode': response.status_code,
            'body': f"Error fetching data: {response.text}"
        }
```

## 5. Lambda-Berechtigungen konfigurieren

Stelle sicher, dass deine Lambda-Rolle die folgenden Berechtigungen hat:

- `S3FullAccess` oder
- spezifische Berechtigungen für den S3 Bucket.

## 6. AWS EventBridge Regel zur Ausführung einer Lambda-Funktion alle 15 Minuten

Um eine AWS Lambda-Funktion alle 15 Minuten mithilfe von **EventBridge** auszuführen, kannst du eine neue Regelzeitplan (Cron-Job) in **EventBridge** erstellen.

### Erstelle eine neue EventBridge-Regel

1. Melde dich bei der AWS Management Console an.
2. Gehe zu **Amazon EventBridge** und klicke auf **Regeln**.
3. Klicke auf **Regel erstellen**.
4. Gib der Regel einen Namen (z. B. `lambda_every_15_minutes`).
5. Wähle unter Regelart die Option **Zeitplan**.

## 7. Lambda-Funktion testen

1. Gehe zur Lambda-Konsole und klicke auf **Test**.
2. Erstelle ein Testevent mit leerem Payload:

   ```json
   {}
   ```

3. Führe die Funktion aus und überprüfe den S3 Bucket, ob die JSON-Datei erfolgreich hochgeladen wurde.

**Fertig!**
