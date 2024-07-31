import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd

#BRUNOMAION
#NORMIE

class PreProcessor:

    def __init__(self) -> None:

        #self.file_directory = 'test_file.mtmtk'
        self.file_directory = input("INSIRA O NOME DO ARQUIVO: ")
        self.text_file = open(f'{self.file_directory}', 'r')
        self.file_content = self.text_file.read()

        self.retornar_conteudo()
        self.print_file_content()

    def retornar_conteudo(self):

        return self.file_content

    def print_file_content(self):

        print(self.file_content)


class AnalisadorLexico:

    def __init__(self) -> None:

        self.PreProcessor = PreProcessor()
        self.file_content = self.PreProcessor.retornar_conteudo()

        self.posicao_cabeca = 0
        self.linha_atual = 1
        self.iteracao_atual = 0

        self.lexema = ''        
        self.fita = self.file_content
        self.log = []

        self.operatores_aritimeticos = ['+', '-', '*', '/', '%']
        self.simbolos_especiais = ['(', ')', '[', ']', '{', '}', ';', '=']
        self.operadores_logicos = ['E', 'OU', 'NAO']
        self.operadores_relacionais = ['IGUAL', 'DIFERENTE', 'MAIOR', 'MAIORIGUAL', 'MENOR', 'MENORIGUAL']
        self.comandos_entrada_saida = ['LEIA', 'IMPRIMA']
        self.estruturas_decisao = ['SE', 'SENAO', 'SENAOSE']
        self.estruturas_repeticao = ['ENQUANTO', 'PARE', 'PARA']

        self.tabela_simbolos = []

        self.q0()

    def avancar_posicao_cabeca(self):

        self.posicao_cabeca += 1

    def retroceder_posicao_cabeca(self):

        self.posicao_cabeca -= 1

    def get_posicao_cabeca(self):

        return self.posicao_cabeca
    
    def atualizar_linha_atual(self):

        self.linha_atual += 1

    def atualizar_log(self, estado, caractere):

        self.log.append(['Iteração = ' + str(self.iteracao_atual), estado, 'Caractere lido = ' + str(caractere)])

    def obter_caractere(self):

        if self.posicao_cabeca < len(self.fita):

            caractere = self.fita[self.posicao_cabeca]

            self.avancar_posicao_cabeca()

            if (caractere != '\n') and (not caractere.isspace()) and (not caractere in self.operatores_aritimeticos) and (not caractere in self.simbolos_especiais):
                self.lexema += caractere
            return caractere
        else:
            return '\n'
        

    def tipo_is_digito(self, caractere):

        return caractere.isdigit()
    
    def tipo_is_operador_aritmetico(self, caractere):

        return caractere in self.operatores_aritimeticos

    def tipo_is_simbolo_especial(self, caractere):

        return caractere in self.simbolos_especiais
    
    def tipo_is_caractere(self, caractere):

        return caractere.isalpha() or caractere == '_'


    def verificar_lexema(self, lexema):

        if lexema in self.operadores_logicos:
            self.tabela_simbolos.append(['OPERADOR_LOGICO', self.lexema, self.linha_atual])
            self.lexema = ''
            self.retroceder_posicao_cabeca()
            self.q0()
        elif lexema in self.operadores_relacionais:
            self.tabela_simbolos.append(['OPERADOR_RELACIONAL', self.lexema, self.linha_atual])
            self.lexema = ''
            self.retroceder_posicao_cabeca()
            self.q0()
        elif lexema in self.comandos_entrada_saida:
            self.tabela_simbolos.append(['ENTRADASAIDA', self.lexema, self.linha_atual])
            self.lexema = ''
            self.retroceder_posicao_cabeca()
            self.q0()
        elif lexema in self.estruturas_decisao:
            self.tabela_simbolos.append(['ESTRUTURA_DECISAO', self.lexema, self.linha_atual])
            self.lexema = ''
            self.retroceder_posicao_cabeca()
            self.q0()
        elif lexema in self.estruturas_repeticao:
            self.tabela_simbolos.append(['ESTRUTURA_REPETICAO', self.lexema, self.linha_atual])
            self.lexema = ''
            self.retroceder_posicao_cabeca()
            self.q0()
        else:
            self.tabela_simbolos.append(['VARIAVEL', self.lexema, self.linha_atual])
            self.lexema = ''
            self.retroceder_posicao_cabeca()
            self.q0()

    def q0(self):
        print('q0')

        self.iteracao_atual += 1
        self.caractere = self.obter_caractere()
        self.atualizar_log('Q0', self.caractere)

        if self.caractere == '\n' and self.posicao_cabeca == len(self.file_content):

            print(self.tabela_simbolos)
            print(self.log)

            df = pd.DataFrame(self.tabela_simbolos, columns=['TIPO', 'LEXEMA', 'LINHA'])
            df.to_csv('dados.csv', index=False, sep=";")


        elif self.tipo_is_digito(self.caractere):

            self.q1()

        elif self.tipo_is_caractere(self.caractere):

            self.q6()

        elif self.tipo_is_operador_aritmetico(self.caractere) or self.tipo_is_simbolo_especial(self.caractere):

            self.tabela_simbolos.append([str(self.caractere), self.caractere, self.linha_atual])
            self.lexema = ''
            self.q0()

        elif self.caractere == '\n':

            self.atualizar_linha_atual()
            self.q0()

        elif self.caractere.isspace():

            self.q0()

    def q1(self):
        print('q1')

        self.iteracao_atual += 1
        self.caractere = self.obter_caractere()
        self.atualizar_log('Q1', self.caractere)  

        if self.tipo_is_digito(self.caractere):
            self.q1()
        elif self.caractere == '.':
            self.q2()
        elif not self.tipo_is_digito(self.caractere):
            self.tabela_simbolos.append(['INTEIRO', self.lexema, self.linha_atual])
            self.lexema = ''
            self.retroceder_posicao_cabeca()
            self.q0()

    def q2(self):
        print('q2')

        self.iteracao_atual += 1
        self.caractere = self.obter_caractere()
        self.atualizar_log('Q2', self.caractere) 

        if self.tipo_is_digito(self.caractere):
            self.q3()

    def q3(self):
        print('q3')

        self.iteracao_atual += 1
        self.caractere = self.obter_caractere()
        self.atualizar_log('Q3', self.caractere) 

        if self.tipo_is_digito(self.caractere):
            self.q3()
        elif not self.tipo_is_digito(self.caractere):
            self.tabela_simbolos.append(['REAL', self.lexema, self.linha_atual])
            self.lexema = ''
            self.retroceder_posicao_cabeca()
            self.q0()

    def q6(self):
        print('q6')

        self.iteracao_atual += 1
        self.caractere = self.obter_caractere()
        self.atualizar_log('Q3', self.caractere) 

        if self.tipo_is_caractere(self.caractere) or self.tipo_is_digito(self.caractere):
            self.q6()
        elif (not self.tipo_is_caractere(self.caractere)) and  (not self.tipo_is_digito(self.caractere)):
            self.verificar_lexema(self.lexema)

    

teste = AnalisadorLexico()

