# Como instalar a skill /gerar-imagem

Com ela você digita `/gerar-imagem` no Claude Code, descreve a imagem, e ela aparece numa pasta do seu computador. Quem gera é o Codex, da OpenAI, usando a assinatura do ChatGPT que você já paga. Não precisa de chave de API e não há cobrança por imagem.

## O que você precisa

- **Claude Code** instalado e funcionando.
- **Assinatura paga do ChatGPT, Plus ou acima.** O plano gratuito não gera imagem pelo Codex. No plano Go a OpenAI não confirma que funciona.
- **Node.js** (para instalar o Codex). Baixe em nodejs.org.
- **Python 3.** No Windows, baixe em python.org e marque "Add Python to PATH" na instalação. No Mac e no Linux ele normalmente já vem.

## Passo 1: instalar o Codex

Abra o terminal (no Windows, o PowerShell) e rode:

```
npm install -g @openai/codex
```

## Passo 2: entrar com a sua conta do ChatGPT

```
codex login
```

O navegador abre. Entre com a mesma conta da sua assinatura do ChatGPT. Para conferir:

```
codex login status
```

Tem que aparecer `Logged in using ChatGPT`.

## Passo 3: colocar a skill no lugar

Baixe o arquivo **gerar-imagem.zip** (https://github.com/Guiair21/gerar-imagem/releases/latest/download/gerar-imagem.zip) e descompacte. Copie a pasta `gerar-imagem` inteira (com o `SKILL.md` e o `gerar_imagem.py` dentro) para a pasta de skills do Claude Code:

- **Windows:** `C:\Users\SEU-USUÁRIO\.claude\skills\gerar-imagem`
- **Mac e Linux:** `~/.claude/skills/gerar-imagem`

Se a pasta `skills` não existir, crie. A pasta `.claude` começa com ponto e fica escondida. No Windows, ative "Itens ocultos" na aba Exibir do Explorador. No Mac, aperte Cmd + Shift + ponto no Finder.

## Passo 4: testar

Feche e abra o Claude Code de novo, numa pasta de projeto qualquer, e digite:

```
/gerar-imagem xícara de café fumegando sobre mesa de madeira, luz de janela, fundo desfocado, sem texto
```

Em cerca de 1 minuto a imagem aparece em `imagens-geradas`, dentro da pasta onde o Claude Code está aberto.

## Como pedir uma imagem boa

Diga três coisas: **o assunto**, **a direção visual** (luz, fundo, enquadramento, estilo) e **o que não pode aparecer**. "Um troféu" dá uma imagem genérica. "Troféu dourado sobre fundo escuro, luz lateral dura, sombra longa, sem texto" dá a imagem que você imaginou.

Você também pode:

- **Editar uma imagem que já existe:** "/gerar-imagem deixa o fundo dessa foto noturno" e o caminho da foto.
- **Pedir variações:** "/gerar-imagem 3 variações de..."
- **Usar a sua identidade visual:** escreva as suas cores, luz e proibições num arquivo `marca.md` e peça para o Claude usar esse estilo.

## O que ela não faz

- **Texto dentro da imagem.** O gerador inventa letras. Faça a imagem sem texto e coloque o texto por cima em outro programa.
- **Tamanho exato.** A proporção sai da descrição ("retrato vertical", "objeto centralizado"). Recorte depois, se precisar.
- **Repetir a mesma imagem.** Cada rodada dá uma imagem diferente.

## Dica bônus: sem ChatGPT pago, use o Claude no Chrome

Se você não tem o Plus, a skill ainda ajuda. Com a extensão **Claude in Chrome** ligada ao Claude Code, o Claude abre o ChatGPT no seu navegador, monta o pedido completo da imagem e deixa tudo escrito na caixa de mensagem. Você só aperta enviar.

1. Instale a extensão Claude in Chrome pela Chrome Web Store e entre com a mesma conta do Claude Code.
2. Abra o Claude Code com `claude --chrome` (ou digite `/chrome` com ele aberto e escolha ligar).
3. No Chrome, entre no chatgpt.com com a sua conta. Pode ser a gratuita.
4. Peça normalmente: `/gerar-imagem xícara de café...`. Sem o Codex, o Claude escreve o pedido no ChatGPT e avisa quando estiver pronto para enviar.

A imagem fica no ChatGPT e sai em menos de 1 minuto. Para baixar, clique na imagem para abrir e use a setinha para baixo no canto de cima, à direita. Pelo plano gratuito o ChatGPT gera poucas imagens por dia. Quando o limite acabar, ele avisa quando libera de novo.

## Se der erro

| O que aparece | O que fazer |
|---|---|
| "o Codex CLI não está instalado" | Refaça o Passo 1. Se o `npm` não existir, instale o Node.js |
| "nenhuma imagem nova" | Rode `codex login status`. Se estiver logado num plano pago, tente de novo com um pedido mais direto |
| O `/gerar-imagem` não aparece no Claude Code | Confira se o `SKILL.md` está em `.claude/skills/gerar-imagem/` e reabra o Claude Code |
| `python` não encontrado (Mac ou Linux) | Peça ao Claude para usar `python3` |

Skill criada por Guilherme Silva (@euguidasilva). Uso livre.
