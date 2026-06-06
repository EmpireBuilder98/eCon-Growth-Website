#!/usr/bin/env python3
"""Generate Jarvis butler voice lines via Microsoft Edge neural TTS.
Uses en-GB-ThomasNeural — formal British male voice.
Outputs MP3 files to assets/audio/jarvis/.
"""
import asyncio
import edge_tts
from pathlib import Path

OUT = Path('/Users/empire-builder98/Jarvis/eCon-Growth-Website/assets/audio/jarvis')
OUT.mkdir(parents=True, exist_ok=True)

VOICE = 'en-GB-ThomasNeural'
RATE = '+12%'   # punchy + energetic — user feedback: was way too slow at -12%
PITCH = '-1Hz' # mildly deeper

LINES = {
    # Virtual guide — Jarvis walks visitors through the site, section by section.
    # Phonetic spelling: "Eecon" → Thomas reads as "EE-CON" (fused word).
    'intro': (
        "Good evening, sir. I am Jarvis. "
        "Allow me to walk you through Eecon Growth — "
        "the operations layer behind serious businesses. "
        "Three service lines. One full stack. Powered by Anthropic's Claude. "
        "Shall we?"
    ),
    'problem': (
        "Every operator faces the same trap, sir. "
        "They become the bottleneck of their own business. "
        "Every decision, every escalation — back on their desk. "
        "Eecon Growth installs the layer that runs without them."
    ),
    'operations': (
        "Operations, sir. "
        "Custom AI Operating Systems for serious operators. "
        "The flagship is Command H-V-A-C — the AI system for H-V-A-C business owners. "
        "Plus the AI Social Media OS, the AI Executive Assistant, "
        "and Roger — the voice agent that answers every call in under three seconds."
    ),
    'marketing': (
        "Marketing services, sir. "
        "Retainers from five hundred a month. "
        "Campaigns, content systems, paid acquisition. "
        "Built quietly. Compounds over time. Hits hard when it matters."
    ),
    'financial': (
        "Financial planning, sir — led by Watson Wheeler, our co-founder. "
        "Business structure for growth. Exit preparation. "
        "The half of the business most operators never plan for."
    ),
    'fullstack': (
        "The thesis, sir. "
        "Most companies sell you one thing. "
        "Eecon Growth builds all three — Operations, Marketing, and Financial — "
        "installed as one system. The result is leverage. Infinite leverage."
    ),
    'founders': (
        "Two operators, sir. "
        "Kristopher Cravens and Watson Wheeler. "
        "Kris spent a decade in the field. "
        "Watson runs strategy, scale, and the financial half. "
        "Built from inside the businesses they serve."
    ),
    'qualify': (
        "This isn't for everyone, sir. "
        "It's for serious operators with real revenue "
        "who want their company to run without them. "
        "If you want a magic button — this isn't it. "
        "If you want infrastructure that holds — keep reading."
    ),
    'faq': (
        "Common questions, sir. Take a moment. "
        "When you're ready, there's a Growth Call button at the bottom. "
        "Thirty minutes. No pitch deck. "
        "Two operators having an honest conversation about your business."
    ),
}

async def gen(name, text):
    out = OUT / f'{name}.mp3'
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH)
    await communicate.save(str(out))
    size = out.stat().st_size // 1024
    print(f'  ✓ {name}.mp3 ({size} KB) — {text[:50]}...')

async def main():
    print(f'Voice: {VOICE} · rate {RATE} · pitch {PITCH}')
    print(f'Output: {OUT}')
    print()
    for name, text in LINES.items():
        await gen(name, text)
    print()
    print('Done. All lines generated.')

asyncio.run(main())
