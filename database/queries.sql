-- ==========================================
-- CONSULTAS DO SISTEMA SISRI
-- ==========================================


-- ==========================================
-- 1. LISTAR TODOS OS SENSORES
-- ==========================================

SELECT *
FROM sensores;



-- ==========================================
-- 2. LISTAR SEMÁFOROS E SENSORES ASSOCIADOS
-- ==========================================

SELECT

semaforo.id,

semaforo.cruzamento,

semaforo.estado,

sensores.identificacao


FROM semaforo

INNER JOIN sensores

ON semaforo.sensor_id = sensores.id;



-- ==========================================
-- 3. LISTAR EVENTOS REGISTRADOS
-- ==========================================

SELECT *

FROM eventos;



-- ==========================================
-- 4. VER DETECÇÕES DA IA
-- ==========================================

SELECT

objeto,

confianca,

data_hora


FROM deteccoes;



-- ==========================================
-- 5. VER MATRÍCULAS DETECTADAS
-- ==========================================

SELECT

numero,

tipo_veiculo,

confianca


FROM matriculas;



-- ==========================================
-- 6. VER ALERTAS GERADOS PELO ECALL
-- ==========================================

SELECT

mensagem,

destino,

estado


FROM alertas;



-- ==========================================
-- 7. RELATÓRIO DE ACIDENTES
-- ==========================================

SELECT

tipo,

COUNT(*) AS quantidade


FROM eventos


GROUP BY tipo;