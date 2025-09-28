## 5. Multi-Câmeras (`multicameras.md`)

**Descrição:** Mostra como várias câmeras alimentam o pipeline simultaneamente.

**Passo a Passo:**

1. Cada câmera captura vídeo.
2. Todos os streams vão para o mesmo pipeline de detecção/embeddings.
3. Tracking/ReID centralizado evita duplicidade de eventos.
4. Eventos consolidados são armazenados no banco.
5. Dashboard exibe todos os eventos integrados.

```mermaid
flowchart TD
    subgraph Cameras
        C1["Câmera 1"]
        C2["Câmera 2"]
        C3["Câmera 3"]
        C4["Câmera 4"]
    end

    subgraph Pipeline
        D["Detecção / Embeddings"]
        R["ReID / Tracking"]
    end

    subgraph Banco
        DB["SQLite / PostgreSQL"]
    end

    subgraph Dashboard
        Dash["Dashboard Web"]
    end

    C1 --> D
    C2 --> D
    C3 --> D
    C4 --> D
    D --> R
    R --> DB
    DB --> Dash
```
