## 2. Fluxo de Embeddings (`embeddings.md`)

**Descrição:** Mostra como as imagens de referência são transformadas em embeddings e como o sistema compara rostos detectados em tempo real para determinar se são permitidos ou não.

**Passo a Passo:**
**Cadastro:**

1. Recebe imagens de referência.
2. Gera embeddings com DeepFace.
3. Salva embeddings no banco com tipo (permitido/não permitido).

**Detecção em Tempo Real:** 4. Câmera captura vídeo. 5. Detecção de rosto com YOLOv8. 6. Alinhamento e pré-processamento. 7. Geração de embedding em tempo real. 8. Comparação com embeddings cadastrados. 9. Distância < threshold → pessoa permitida. 10. Distância ≥ threshold → pessoa não permitida, alerta.

```mermaid
flowchart TD
    subgraph Cadastro
        Img["Imagens de Referência"] --> GenEmb["Gerar Embeddings (DeepFace)"]
        GenEmb --> DB["Banco de Dados (SQLite / PostgreSQL)"]
        Tipo["Tipo: Permitido/Não Permitido"] --> DB
    end

    subgraph Detecção_RealTime
        Cam["Câmera IP / Stream"] --> Detect["Detecção de Rosto (YOLOv8)"]
        Detect --> Align["Alinhamento / Pré-processamento"]
        Align --> GenEmbRT["Gerar Embedding em Tempo Real (DeepFace)"]
        GenEmbRT --> Compare["Comparar com Embeddings do Banco"]
        Compare --> Resultado{"Distância < Threshold?"}
        Resultado -->|Sim| Permitido["Pessoa Permitida"]
        Resultado -->|Não| NPermitido["Pessoa Não Permitida / Alerta"]
    end

    DB --> Compare
```
