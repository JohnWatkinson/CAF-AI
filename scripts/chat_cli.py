#!/usr/bin/env python3
"""
CLI for testing the IMU chat assistant.
Usage: python scripts/chat_cli.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from src.chat.engine import ChatEngine


def main():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Errore: ANTHROPIC_API_KEY non trovata. Crea un file .env con la chiave.")
        sys.exit(1)

    engine = ChatEngine(api_key=api_key)
    print("=== Assistente IMU ===")
    print("Scrivi 'quit' per uscire, 'reset' per ricominciare.\n")

    # Start the conversation
    response = engine.send_message("Ciao, devo calcolare l'IMU")
    print(f"Assistente: {response}\n")

    while True:
        try:
            user_input = input("Tu: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nCiao!")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("Ciao!")
            break
        if user_input.lower() == "reset":
            engine.reset()
            print("--- Conversazione resettata ---\n")
            response = engine.send_message("Ciao, devo calcolare l'IMU")
            print(f"Assistente: {response}\n")
            continue

        response = engine.send_message(user_input)
        print(f"\nAssistente: {response}\n")


if __name__ == "__main__":
    main()
