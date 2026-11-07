# AcquaCEG Backend

> FastAPI backend responsible for processing AcquaCEG sensor data, integrating MQTT communication, data validation, PostgreSQL storage and REST API services.

---

## 🇺🇸 English

## Overview

AcquaCEG Backend is the server-side application responsible for receiving, processing and storing sensor data collected by the AcquaCEG monitoring ecosystem.

The application subscribes to MQTT topics, validates incoming measurements, converts raw sensor values into engineering units and stores the processed data in a PostgreSQL database.

It also exposes a REST API that allows external applications such as dashboards and mobile apps to access historical and real-time information.

---

## Features

- MQTT subscriber
- Sensor data validation
- Data conversion
- PostgreSQL integration
- REST API with FastAPI
- Modular architecture
- Environment variable configuration
- Cloud-ready architecture

---

# Architecture

```
Arduino Uno R4 WiFi
        │
        ▼
 MQTT over TLS
        │
        ▼
   EMQX Cloud
        │
        ▼
 AcquaCEG Backend
        │
 ┌──────┴──────┐
 ▼             ▼
Validation   Processing
        │
        ▼
 PostgreSQL Database
        │
        ▼
     REST API
        │
 ┌──────┴──────┐
 ▼             ▼
Dashboard   Mobile App
```

---

## Technologies

### Backend

- Python
- FastAPI
- SQLAlchemy

### Database

- PostgreSQL

### Communication

- MQTT
- EMQX Cloud

### Development

- Uvicorn
- Python Dotenv

---

## Project Structure

```
app/
├── api/
├── core/
├── database/
├── models/
├── mqtt/
├── routes/
├── schemas/
├── services/
└── main.py

config/
tests/

requirements.txt
run.py
```

---

## Running the Project

### Clone the repository

```bash
git clone https://github.com/AcquaCEG/AcquaCEG-Backend.git
cd AcquaCEG-Backend
```

### Create the virtual environment

```bash
py -m venv .venv
```

### Activate the virtual environment

**Windows**

```bash
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql+psycopg2://usuario:senha@host:5432/banco

MQTT_BROKER=
MQTT_PORT=
MQTT_CLIENT_ID=
MQTT_USERNAME=
MQTT_PASSWORD=
MQTT_TOPIC=
```

### Start the server

```bash
uvicorn app.main:app --reload
```

---

## Future Improvements

- Authentication and authorization
- Multiple monitored devices
- Notification system
- AI-assisted monitoring
- Dashboard integration
- Cloud deployment

---

## License

Distributed under the MIT License.

---

# 🇧🇷 Português

## Visão Geral

O AcquaCEG Backend é a aplicação responsável por receber, processar e armazenar os dados enviados pelos sensores do ecossistema AcquaCEG.

O sistema se conecta ao broker MQTT, recebe as leituras dos dispositivos embarcados, valida e converte os dados para unidades de engenharia e armazena todas as informações em um banco de dados PostgreSQL.

Além disso, disponibiliza uma API REST desenvolvida com FastAPI para que dashboards, aplicações móveis e outros serviços possam acessar as medições em tempo real e o histórico de leituras.

---

## Funcionalidades

- Assinatura de tópicos MQTT
- Validação das leituras dos sensores
- Conversão dos dados
- Integração com PostgreSQL
- API REST utilizando FastAPI
- Arquitetura modular
- Configuração através de variáveis de ambiente
- Preparado para execução em nuvem

---

# Arquitetura

```
Arduino Uno R4 WiFi
        │
        ▼
 MQTT sobre TLS
        │
        ▼
    EMQX Cloud
        │
        ▼
 AcquaCEG Backend
        │
 ┌──────┴──────┐
 ▼             ▼
Validação  Processamento
        │
        ▼
 PostgreSQL
        │
        ▼
     API REST
        │
 ┌──────┴──────┐
 ▼             ▼
Dashboard   Aplicativo
```

---

## Tecnologias

### Backend

- Python
- FastAPI
- SQLAlchemy

### Banco de Dados

- PostgreSQL

### Comunicação

- MQTT
- EMQX Cloud

### Desenvolvimento

- Uvicorn
- Python Dotenv

---

## Estrutura do Projeto

```
app/
├── api/
├── core/
├── database/
├── models/
├── mqtt/
├── routes/
├── schemas/
├── services/
└── main.py

config/
tests/

requirements.txt
run.py
```

---

## Executando o Projeto

### Clonar o repositório

```bash
git clone https://github.com/AcquaCEG/AcquaCEG-Backend.git
cd AcquaCEG-Backend
```

### Criar o ambiente virtual

```bash
py -m venv .venv
```

### Ativar o ambiente virtual

```bash
.\.venv\Scripts\Activate.ps1
```

### Instalar as dependências

```bash
pip install -r requirements.txt
```

### Configurar o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto.

Exemplo:

```env
DATABASE_URL=postgresql+psycopg2://usuario:senha@host:5432/banco

MQTT_BROKER=
MQTT_PORT=
MQTT_CLIENT_ID=
MQTT_USERNAME=
MQTT_PASSWORD=
MQTT_TOPIC=
```

### Executar a aplicação

```bash
uvicorn app.main:app --reload
```

---

## Melhorias Futuras

- Autenticação e autorização
- Suporte a múltiplos dispositivos
- Sistema de notificações
- Monitoramento assistido por IA
- Integração com dashboards
- Implantação em nuvem

---

## Licença

Distribuído sob a licença MIT.
