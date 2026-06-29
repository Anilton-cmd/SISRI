-- ==========================================
-- SISTEMA INTEGRADO DE SEGURANÇA RODOVIÁRIA
-- INTELIGENTE - SISRI

-- ==========================================


-- ===============================
-- TABELA DE UTILIZADORES
-- ===============================

CREATE TABLE utilizadores (

    id SERIAL PRIMARY KEY,

    nome VARCHAR(100) NOT NULL,

    email VARCHAR(100) UNIQUE,

    perfil VARCHAR(50),

    senha TEXT,

    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- ===============================
-- TABELA DE SENSORES/CÂMERAS
-- ===============================

CREATE TABLE sensores (

    id SERIAL PRIMARY KEY,

    tipo VARCHAR(50) NOT NULL,

    identificacao VARCHAR(100),

    localizacao VARCHAR(150),

    estado VARCHAR(30),

    data_instalacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- ===============================
-- TABELA DE SEMÁFOROS INTELIGENTES
-- ===============================

CREATE TABLE semaforo (

    id SERIAL PRIMARY KEY,

    sensor_id INTEGER,

    cruzamento VARCHAR(150),

    estado VARCHAR(20),

    tempo_ativo INTEGER,

    modo_funcionamento VARCHAR(50),

    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT fk_semaforo_sensor

    FOREIGN KEY(sensor_id)

    REFERENCES sensores(id)

);



-- ===============================
-- TABELA DE EVENTOS RODOVIÁRIOS
-- ===============================

CREATE TABLE eventos (

    id SERIAL PRIMARY KEY,


    semaforo_id INTEGER,


    tipo VARCHAR(100),


    descricao TEXT,


    gravidade VARCHAR(30),


    localizacao VARCHAR(150),


    estado VARCHAR(30),


    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT fk_evento_semaforo

    FOREIGN KEY(semaforo_id)

    REFERENCES semaforo(id)

);



-- ===============================
-- TABELA DE DETECÇÕES DA IA
-- ===============================

CREATE TABLE deteccoes (

    id SERIAL PRIMARY KEY,


    evento_id INTEGER,


    sensor_id INTEGER,


    objeto VARCHAR(50),


    confianca FLOAT,


    quantidade INTEGER,


    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT fk_deteccao_evento

    FOREIGN KEY(evento_id)

    REFERENCES eventos(id),



    CONSTRAINT fk_deteccao_sensor

    FOREIGN KEY(sensor_id)

    REFERENCES sensores(id)

);



-- ===============================
-- TABELA DE MATRÍCULAS
-- ===============================

CREATE TABLE matriculas (

    id SERIAL PRIMARY KEY,


    deteccao_id INTEGER,


    numero VARCHAR(30),


    tipo_veiculo VARCHAR(50),


    confianca FLOAT,


    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT fk_matricula_deteccao

    FOREIGN KEY(deteccao_id)

    REFERENCES deteccoes(id)

);



-- ===============================
-- SISTEMA DE ALERTAS eCALL
-- ===============================

CREATE TABLE alertas (

    id SERIAL PRIMARY KEY,


    evento_id INTEGER,


    destino VARCHAR(100),


    mensagem TEXT,


    estado VARCHAR(30),


    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT fk_alerta_evento

    FOREIGN KEY(evento_id)

    REFERENCES eventos(id)

);



-- ===============================
-- LOGS DO SISTEMA
-- ===============================

CREATE TABLE logs (

    id SERIAL PRIMARY KEY,


    utilizador_id INTEGER,


    modulo VARCHAR(50),


    mensagem TEXT,


    nivel VARCHAR(20),


    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT fk_log_utilizador

    FOREIGN KEY(utilizador_id)

    REFERENCES utilizadores(id)

);