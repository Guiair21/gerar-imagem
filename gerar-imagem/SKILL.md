---
name: gerar-imagem
description: >
  Use quando o usuário pedir uma imagem gerada por inteligência artificial: foto conceitual,
  ilustração, objeto, textura, fundo, cenário, ou a edição e a variação de uma imagem que já
  existe. Dispare com "/gerar-imagem", "gera uma imagem de", "cria uma arte de", "faz uma foto
  de", "edita essa imagem". Não use para peça com texto dentro (card, carrossel, slide, banner),
  porque o gerador inventa letras.
---

# /gerar-imagem: Claude Code → Codex → imagem na sua pasta

O Claude Code não gera imagem. O Codex CLI gera, pela ferramenta `image_gen`, dentro dos
limites da assinatura do ChatGPT, sem chave de API e sem cobrança por imagem. O
`gerar_imagem.py`, nesta mesma pasta, faz a ponte e põe a imagem na pasta certa.

Requisitos: Codex CLI instalado (`npm install -g @openai/codex`), login feito com uma conta
paga do ChatGPT (`codex login`; Plus ou acima) e Python 3.

## A sequência

**1. Travar o briefing antes de rodar.** O briefing é o texto que vai entre aspas no comando,
em português ou inglês, com três coisas: o assunto, a direção visual (luz, fundo,
enquadramento, estilo) e o que não pode aparecer. Se o pedido for vago, pergunte só o que
faltar. Se não der para perguntar, complete a direção visual e as proibições você mesmo e
diga ao usuário, numa linha, o que assumiu. Briefing vago dá imagem genérica.

Para a proporção, comece o briefing com "retrato vertical:" ou "horizontal, panorâmico:".
Não existe opção de tamanho.

**2. Rodar o script** (troque `<pasta da skill>` pelo caminho desta pasta):

```bash
python "<pasta da skill>/gerar_imagem.py" "troféu dourado sobre fundo escuro, luz lateral dura, sombra longa, sem texto" --nome trofeu --abrir
```

| Opção | Para quê |
|---|---|
| `--saida PASTA` | onde salvar (padrão: `./imagens-geradas`) |
| `--nome` | nome do arquivo; o padrão sai do briefing |
| `--ref imagem.png` | edição: parte de uma imagem que já existe. Pode repetir |
| `--variacoes N` | N imagens numa chamada só |
| `--estilo marca.md` | injeta a sua identidade visual (cores, luz, proibições) antes do briefing |
| `--seco` | mostra o prompt e o comando sem gastar nada |
| `--abrir` | abre a pasta no fim |

No Mac e no Linux, use `python3` se `python` não existir. Dê ao comando um tempo limite de
10 minutos: a geração costuma levar 1 minuto, mas pode passar disso. Use `--abrir` só quando o
usuário estiver no computador e quiser ver a pasta.

**3. Olhar a imagem antes de entregar.** Abra o PNG e confira: mão com dedo a mais, letra
inventada no fundo, objeto deformado. O script imprime um JSON com o caminho de cada arquivo.

## Plano B: sem Codex, pelo ChatGPT no Chrome

Use quando o Codex não estiver instalado, quando o login não for de um plano pago ou quando o
usuário pedir. Precisa das ferramentas do Claude in Chrome (`mcp__claude-in-chrome__*`); sem
elas, explique o passo 1 deste plano e pare.

1. Trave o briefing do mesmo jeito do passo 1 e escreva o pedido final assim:
   "Gere uma imagem: <briefing>".
2. Abra uma aba nova em https://chatgpt.com. Se aparecer a tela de login, peça ao usuário para
   entrar e espere. Quem loga é sempre o usuário.
3. Escreva o pedido na caixa de mensagem do ChatGPT e pare. **Não clique em enviar.** Diga ao
   usuário que o pedido está pronto e que é só apertar enviar.
4. Avise que a imagem fica no ChatGPT. Para baixar: clicar na imagem para abrir o visualizador
   e usar a seta de download no canto superior direito. Se o usuário pedir para você enviar e
   baixar, faça o mesmo caminho e procure o arquivo na pasta de downloads.

## O que a ferramenta não faz

- **Não escolhe tamanho nem proporção.** O modelo decide pelo texto: "objeto centralizado"
  costuma sair quadrado, "retrato vertical" sai em pé. Formato final é recorte depois.
- **Não repete resultado.** Não há seed: o mesmo briefing dá imagens diferentes.
- **Não escreve bem.** Texto vai por cima depois, em outro programa.

## Tempo e custo

Cada imagem leva por volta de 1 minuto (às vezes até 3) e gasta o limite de uso da assinatura do ChatGPT, não
dinheiro por imagem. Num lote grande, avise o tempo antes de disparar.

## Quando der errado

| Sintoma | Causa e saída |
|---|---|
| "o Codex CLI não está instalado" | `npm install -g @openai/codex` (precisa do Node.js) |
| "nenhuma imagem nova" | o Codex respondeu em texto em vez de gerar. Rode `codex login status` (plano gratuito não gera imagem), depois rode de novo com `--seco`, leia o prompt e deixe o pedido mais direto |
| Windows: "setup refresh had errors" | o script já usa o sandbox `unelevated`; atualize o Codex |
| Duas imagens com sufixo `-2` | o Codex às vezes gera duas numa chamada. Olhe as duas antes de escolher |
| Editar com `--ref` uma imagem da própria pasta de saída | copie a referência para outra pasta antes, para não perder a original |

Criada por Guilherme Silva (@euguidasilva).
