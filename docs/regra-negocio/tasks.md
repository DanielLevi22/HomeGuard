# HomeGuard – Lista de Tarefas Detalhadas

> Cada tarefa possui um **NV (Nível de Implementação / Prioridade)** de 1 a 5, sendo 1 a mais urgente.
> Campo de status: `[ ] Concluída`

---

## 1. Cadastro de Pessoas

- [ ] Criar modelo de dados para pessoas no banco (NV: 1)
- [ ] Implementar API para cadastrar pessoa (NV: 1)
- [ ] Criar front-end para cadastro (NV: 2)
- [ ] Implementar upload de fotos e validação (NV: 1)
- [ ] Gerar embeddings das imagens ao cadastrar (NV: 1)
- [ ] Implementar edição de status (permitido/não permitido) (NV: 2)
- [ ] Implementar remoção de pessoa (NV: 2)

---

## 2. Detecção e Reconhecimento

- [ ] Configurar captura de vídeo da câmera IP (NV: 1)
- [ ] Integrar YOLOv8 para detectar rosto e corpo (NV: 1)
- [ ] Implementar alinhamento de rosto (NV: 2)
- [ ] Implementar DeepFace para reconhecimento facial (NV: 1)
- [ ] Integrar tracking/ReID (DeepSORT/ByteTrack) (NV: 2)
- [ ] Implementar fallback para rosto coberto ou ângulo ruim (NV: 3)
- [ ] Registrar eventos com timestamp e câmera (NV: 1)

---

## 3. Alertas

- [ ] Disparar alertas para pessoas não permitidas (NV: 1)
- [ ] Integrar Telegram API (NV: 2)
- [ ] Integrar envio de Email (NV: 2)
- [ ] Atualizar dashboard em tempo real (NV: 1)
- [ ] Adicionar foto/frame da detecção nos alertas (NV: 2)

---

## 4. Multi-Câmeras

- [ ] Configurar pipeline para múltiplas câmeras (NV: 1)
- [ ] Consolidar eventos duplicados (NV: 2)
- [ ] Configurar proximidade de detecção por câmera (NV: 3)

---

## 5. Embeddings

- [ ] Atualizar embeddings continuamente para pessoas cadastradas (NV: 3)
- [ ] Arquivar embeddings antigos para auditoria (NV: 4)
- [ ] Comparação em tempo real no pipeline (NV: 1)

---

## 6. Fallback / Anti-Fraude

- [ ] Implementar tracking/ReID quando rosto não detectado (NV: 3)
- [ ] Registrar desconhecidos e disparar alerta (NV: 2)
- [ ] Adicionar proteção contra spoofing (fotos/vídeos) (NV: 4)
