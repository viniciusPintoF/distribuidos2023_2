# Especificações 
* Os comandos são reconhecidos por 1 byte
* Os valores das contas serão floats com precisão de duas casas decimais (importante especificar por conta da maneira como python usa float)
* Os comandos terão tamanho pre-determinado e fixo
* O clock lógico de Lamport será utilizado e representado por um inteiro no final de cada mensagem trocada
# Exemplo de mensagem:
[COMANDO(1byte)RG(INTEIRO)VALOR(FLOAT)CLOCK(INTEIRO)]
