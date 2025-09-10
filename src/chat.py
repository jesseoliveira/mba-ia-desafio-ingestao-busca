# ================================================================== #
# Desafio MBA Engenharia de Software com IA - Full Cycle             #
# ================================================================== #
# Autor: Jesse de Oliveira                                           #
# Email: jesse.oli@hotmail.com                                       #
# Data: 03/09/2025                                                   #
# Versão: 1.0.0                                                      #
# ================================================================== # 

from search import search_prompt

def main():
    print("="*80)
    print(" " * 15 + "Desafio MBA Engenharia de Software com IA - Full Cycle")
    print(" " * 22 + "Bem-vindo ao nosso chat via terminal!")
    print(" " * 22 + "Quando quiser encerrar, digite 'sair'")
    print("="*80)
    n_questions = 1
    while True:
        question = input(str(n_questions)+") Faça sua pergunta (digite 'sair' para encerrar): ").lower()
        if question == "sair":
            print("\nFoi um prazer conversar com você. Até logo!\n")
            print("="*80)
            break
        response = search_prompt(question)
        print("Resposta: "+response+"\n")
        n_questions += 1

if __name__ == "__main__":
    main()