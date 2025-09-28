# HomeGuard – Regras de Negócio

> Campo de status: [ ] Concluída
> (Marque quando a funcionalidade estiver implementada e testada)

## 1. Cadastro de Pessoas

> Status: [ ]

- Cada pessoa deve ser classificada como:

  - **Permitida**: pode transitar livremente, sem gerar alertas.
  - **Não Permitida**: qualquer detecção gera alerta imediato.

- As imagens de referência devem ser de boa qualidade e incluir diferentes ângulos do rosto.
- Embeddings são atualizados automaticamente quando novas imagens são adicionadas.
- É possível remover ou alterar o status de uma pessoa a qualquer momento.

## 2. Detecção e Reconhecimento

> Status: [ ]

- A detecção inicial utiliza YOLOv8 para identificar rostos e pessoas.
- Se o rosto estiver visível, usa DeepFace para reconhecimento facial.
- Se o rosto não estiver visível ou coberto, utiliza ReID/Tracking para identificar pelo corpo ou movimento.
- Cada pessoa é registrada no banco de dados com **timestamp** e **câmera de origem**.
- Distância de embeddings define se a pessoa é permitida ou não:

  - **< Threshold:** permitida.
  - **>= Threshold:** não permitida.

## 3. Alertas

> Status: [ ]

- Alertas devem ser disparados para qualquer pessoa **não permitida**.
- Tipos de alertas:

  - **Telegram**: notificação instantânea.
  - **Email**: envio detalhado de evento.
  - **Dashboard**: atualização em tempo real.

- Alertas devem incluir:

  - Foto ou frame da pessoa detectada.
  - Hora e câmera da detecção.
  - Status (permitida / não permitida).

## 4. Multi-Câmeras

> Status: [ ]

- Todas as câmeras alimentam o mesmo pipeline centralizado.
- Eventos duplicados de diferentes câmeras para a mesma pessoa devem ser consolidados.
- Cada câmera possui seu campo de visão e pode ter configurações de proximidade para detecção.

## 5. Embeddings

> Status: [ ]

- Cada pessoa possui embeddings atualizados continuamente para aumentar a precisão.
- Embeddings antigos podem ser arquivados para auditoria.
- Comparação é feita em tempo real para detectar se a pessoa é permitida ou não.

## 6. Fallback / Anti-Fraude

> Status: [ ]

- Caso o rosto não seja detectado:

  - O sistema utiliza tracking/ReID para identificar pelo corpo.
  - Se não for possível identificar, registra como **desconhecido** e dispara alerta.

- O sistema deve ser resistente a tentativas de **spoofing** (fotos ou vídeos de pessoas permitidas).
