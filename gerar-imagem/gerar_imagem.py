#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_imagem.py: ponte Claude Code -> Codex CLI (ferramenta image_gen) -> arquivo na sua pasta.

O Codex salva toda imagem em CODEX_HOME/generated_images/<thread>/exec-*.png e não aceita
caminho de destino. O --json também não devolve o caminho do arquivo. Por isso quem decide o
destino é este script: ele lê o thread_id que o Codex anuncia no --json e copia só as
imagens daquele thread, mesmo com várias gerações rodando ao mesmo tempo.

Criado por Guilherme Silva (@euguidasilva). Uso livre.
"""
import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import unicodedata
from datetime import date
from pathlib import Path

WINDOWS = platform.system() == "Windows"


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or (Path.home() / ".codex"))


def fotografar(raiz: Path) -> set:
    if not raiz.exists():
        return set()
    return set(raiz.rglob("*.png"))


def slugificar(txt: str, limite: int = 48) -> str:
    txt = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode()
    txt = re.sub(r"[^a-zA-Z0-9]+", "-", txt).strip("-").lower()
    return (txt[:limite].rstrip("-")) or "imagem"


def montar_prompt(args) -> str:
    partes = []
    if args.estilo:
        partes.append("IDENTIDADE VISUAL (siga sempre):\n" + Path(args.estilo).read_text(encoding="utf-8").strip())
    partes.append("BRIEFING DA IMAGEM:\n" + args.briefing.strip())
    if args.ref:
        caminhos = "\n".join(f"- {Path(r).resolve()}" for r in args.ref)
        partes.append(
            "EDIÇÃO: parta das imagens abaixo, passando os caminhos em "
            "referenced_image_paths:\n" + caminhos
        )
    if args.variacoes > 1:
        partes.append(
            f"Gere {args.variacoes} variações desta mesma ideia, uma chamada da "
            "ferramenta por variação. Varie composição e enquadramento, não o assunto."
        )
    partes.append(
        "COMO EXECUTAR: use a ferramenta integrada image_gen (built-in). Não use a API, "
        "não escreva código e não instale nada. Não copie, não mova e não renomeie arquivo "
        "nenhum: o destino final é responsabilidade do script que te chamou. Ao terminar, "
        "responda só com a contagem de imagens geradas."
    )
    return "\n\n".join(partes)


def comando_codex(args, destino: Path, ultima_msg: Path) -> list:
    codex = shutil.which("codex")
    if not codex:
        sys.exit("ERRO: o Codex CLI não está instalado. Rode: npm install -g @openai/codex")
    # no Windows o codex é um .cmd; pelo cmd.exe ele roda igual em qualquer versão do Python
    cmd = (["cmd.exe", "/c", "codex"] if WINDOWS else [codex]) + ["exec", "--skip-git-repo-check"]
    if WINDOWS:
        # o sandbox "elevated" do Windows falha com "setup refresh had errors" em algumas máquinas
        cmd += ["-c", f'windows.sandbox="{args.sandbox}"']
    if args.modelo:
        cmd += ["-m", args.modelo]
    # --disable apps: sem isso o Codex às vezes tenta gerar por um conector (Canva etc.) e para pedindo aprovação
    cmd += ["--enable", "image_generation", "--disable", "apps", "--json",
            "-C", str(destino), "-o", str(ultima_msg)]
    for r in args.ref:
        cmd += ["--add-dir", str(Path(r).resolve().parent)]
    cmd.append("-")  # o prompt vai pelo stdin: aspas e acentos não quebram
    return cmd


def abrir_pasta(pasta: Path) -> None:
    if WINDOWS:
        os.startfile(str(pasta))  # noqa: S606
    elif platform.system() == "Darwin":
        subprocess.run(["open", str(pasta)], check=False)
    else:
        subprocess.run(["xdg-open", str(pasta)], check=False)


def main() -> int:
    # o terminal do Windows nem sempre está em UTF-8; sem isso os acentos saem trocados na tela
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except AttributeError:
            pass
    ap = argparse.ArgumentParser(description="Gera imagem pelo Codex CLI e salva na pasta que você escolher.")
    ap.add_argument("briefing", help="descrição da imagem")
    ap.add_argument("--saida", default="imagens-geradas",
                    help="pasta de destino (padrão: ./imagens-geradas)")
    ap.add_argument("--nome", help="nome do arquivo final; padrão vem do briefing")
    ap.add_argument("--estilo", help="arquivo .md ou .txt com a sua identidade visual, injetado antes do briefing")
    ap.add_argument("--ref", action="append", default=[], help="imagem de referência para edição (repetível)")
    ap.add_argument("--variacoes", type=int, default=1, help="quantas imagens gerar na mesma chamada")
    ap.add_argument("--timeout", type=int, default=900, help="segundos até desistir (padrão 900)")
    ap.add_argument("--abrir", action="store_true", help="abre a pasta de destino no fim")
    ap.add_argument("--seco", action="store_true", help="mostra o prompt e o comando, sem gerar nada")
    ap.add_argument("--modelo", default=None, help="modelo do Codex (padrão: o do seu config.toml)")
    ap.add_argument("--sandbox", default="unelevated", help="só Windows: windows.sandbox do Codex")
    args = ap.parse_args()

    for r in args.ref:
        if not Path(r).is_file():
            sys.exit(f"ERRO: imagem de referência não encontrada: {r}")
    if args.estilo and not Path(args.estilo).is_file():
        sys.exit(f"ERRO: arquivo de estilo não encontrado: {args.estilo}")

    destino = Path(args.saida).resolve()
    prompt = montar_prompt(args)
    raiz_img = codex_home() / "generated_images"
    ultima_msg = destino / ".codex-ultima-msg.txt"
    cmd = comando_codex(args, destino, ultima_msg)

    if args.seco:
        print("COMANDO:", " ".join(cmd))
        print("\nPROMPT:\n" + prompt)
        return 0

    destino.mkdir(parents=True, exist_ok=True)
    antes = fotografar(raiz_img)
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, input=prompt.encode("utf-8"), capture_output=True, timeout=args.timeout)
    except subprocess.TimeoutExpired:
        print(f"ERRO: o Codex passou de {args.timeout}s sem terminar.", file=sys.stderr)
        return 3
    segundos = round(time.time() - t0, 1)

    thread = None
    saida = proc.stdout.decode("utf-8", "replace")
    for linha in saida.splitlines():
        if '"thread.started"' in linha:
            try:
                thread = json.loads(linha).get("thread_id")
            except json.JSONDecodeError:
                pass
    if thread and (raiz_img / thread).exists():
        novos = sorted((raiz_img / thread).glob("*.png"), key=lambda p: p.stat().st_mtime)
    else:
        novos = sorted(fotografar(raiz_img) - antes, key=lambda p: p.stat().st_mtime)

    if ultima_msg.exists():
        ultima_msg.unlink()

    if not novos:
        print(f"ERRO: nenhuma imagem nova em {raiz_img} depois de {segundos}s.", file=sys.stderr)
        print("Confira se você está logado com uma conta paga do ChatGPT (codex login status).", file=sys.stderr)
        print("--- saída do codex ---", file=sys.stderr)
        print(saida[-2000:], file=sys.stderr)
        print(proc.stderr.decode("utf-8", "replace")[-1000:], file=sys.stderr)
        return 2

    base = args.nome or slugificar(args.briefing)
    hoje = date.today().strftime("%Y-%m-%d")
    finais = []
    for origem in novos:
        n = 1
        while True:
            alvo = destino / f"{hoje}-{base}{'' if n == 1 else f'-{n}'}.png"
            if not alvo.exists():
                break
            n += 1
        shutil.copy2(origem, alvo)
        finais.append(str(alvo))

    print(json.dumps({"arquivos": finais, "destino": str(destino), "segundos": segundos, "thread": thread},
                     ensure_ascii=False, indent=2))
    if args.abrir:
        abrir_pasta(destino)
    return 0


if __name__ == "__main__":
    sys.exit(main())
