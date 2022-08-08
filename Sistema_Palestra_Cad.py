#bibliotecas
import sqlite3 
from tkinter import*
from tkinter import ttk
#cria a janela
janela = Tk()
#inserindo funçôes para os botões
class Funcoes_dos_bot():    
    def limpar_tela_bt(self):
        #self.cod_entrada.delete(0,END)
        self.ra_entrada.delete(0,END)
        self.nome_entrada.delete(0,END)
        self.curso_entrada.delete(0,END)
        self.email_entrada.delete(0,END)    
    #banco de dados
    def conecta_banco_de_dados(self):
        self.conn = sqlite3.connect('Palestra.bd')
        self.cursor = self.conn.cursor()    
    def desconectar_banco(self):
        self.conn.close()
    def estruturarTabela(self):
        self.conecta_banco_de_dados()
        print("conectando ao Banco....")
        ###criando os campos da tabela-
        self.cursor.execute ("""
            CREATE TABLE IF NOT EXISTS Palestra (
            RA INTEGER(7),
            Nome CHAR(40),
            curso CHAR(40),
            email CHAR(40)
            );
        """)
        self.conn.commit()
        print('Banco de dados criado!')
        self.desconectar_banco()
        print('Banco de dados desconectado!')
    #agilzar o uso das das dunções
    def agi_variavel_(self):
        #self.cod = self.cod_entrada.get()
        self.ra = self.ra_entrada.get()
        self.nome = self.nome_entrada.get()
        self.curso = self.curso_entrada.get()
        self.email = self.email_entrada.get()            
    #adiconando informações no banco
    def adicionar_aluno(self):
        self.agi_variavel_()
        self.conecta_banco_de_dados()        
        self.cursor.execute(""" INSERT INTO Palestra (RA,Nome,curso,email)
                            VALUES(?,?,?,?) 
                            """,(self.ra,self.nome,self.curso,self.email,))
        self.conn.commit()
        self.desconectar_banco()
        self.selecionando_lista()
        self.limpar_tela_bt()       
    #selecionando informações no banco
    def selecionando_lista(self):
        self.lista_Aluno_Cads.delete(*self.lista_Aluno_Cads.get_children())
        self.conecta_banco_de_dados()
        lista = self.cursor.execute(""" SELECT RA,Nome,curso,email FROM Palestra
                                     ORDER BY Nome ASC;""")
        for i in lista:
            self.lista_Aluno_Cads.insert("",END, value=i)
        self.desconectar_banco()
    def duploclique_apagar(self,event):
            self.limpar_tela_bt()
            self.lista_Aluno_Cads.selection()  
            
            for n in self.lista_Aluno_Cads.selection():
                col1,col2,col3,col4 = self.lista_Aluno_Cads.item(n,'values')
                self.ra_entrada.insert(END, col1) 
                self.nome_entrada.insert(END, col2)
                self.curso_entrada.insert(END, col3)
                self.email_entrada.insert(END, col4)
    def apagar_cad(self):
        self.agi_variavel_()
        self.conecta_banco_de_dados()
        self.cursor.execute("""DELETE FROM palestra WHERE RA =?
                            """,(self.ra,))
        self.conn.commit()
        self.desconectar_banco()
        self.limpar_tela_bt()
        self.selecionando_lista()                                       
    def alterar_cad(self):
        self.agi_variavel_()
        self.conecta_banco_de_dados()
    
        self.cursor.execute("""UPDATE Palestra SET RA= ?,Nome= ?, curso= ?, email= ? 
                        WHERE RA= ?""", (self.ra,self.nome,self.curso,self.email,self.ra,))
        self.conn.commit()
        self.desconectar_banco()
        self.selecionando_lista()
        self.limpar_tela_bt()
    def buscar_aluno(self):
            self.conecta_banco_de_dados()
            
            self.lista_Aluno_Cads.delete(*self.lista_Aluno_Cads.get_children())
            
            self.nome_entrada.insert(END,'%')
            nome = self.nome_entrada.get()
            self.cursor.execute(
                                """SELECT RA,Nome,curso,email FROM Palestra
                                WHERE Nome LIKE '%s' ORDER BY Nome ASC""" % nome)
            buscanomeAlu = self.cursor.fetchall()
            for i in buscanomeAlu:
                self.lista_Aluno_Cads.insert("",END, values=i)
            self.limpar_tela_bt()
            self.desconectar_banco()
class APlicacaoCadastro(Funcoes_dos_bot):
    #função para chamar os demais componentes
    def __init__(self):
        self.janela = janela
        self._tela_()
        self._frame_da_tela()
        self._botton_da_tela_frame_01()
        self._label_do_frame_01()
        self.lista_frame_02()
        self.estruturarTabela()
        self.selecionando_lista()
        self._menus()
        self.buscar_aluno() 
        janela.mainloop()
    #configurações da tela principal
    def _tela_(self):
        self.janela.title("Bem-vindo ao nosso sistema de cadastro de palestras universitárias")
        self.janela.configure(background='#B0E0E6')
        self.janela.geometry('700x500')
        self.janela.resizable(False,False)
        self.janela.maxsize(width='900',height='700')
        self.janela.minsize(width='400',height='300')
    #frames inferior e superior
    def _frame_da_tela(self):
        self.frame_1 = Frame(self.janela,bd= 4,bg='#F5FFFA',highlightbackground='#FFFACD',highlightthickness= 3)
        self.frame_1.place(relx=0.02,rely=0.02, relheight=0.46,relwidth=0.96)
        
        self.frame_2 = Frame(self.janela,bd= 4,bg='#F5FFFA',highlightbackground='#FFFACD',highlightthickness= 3)
        self.frame_2.place(relx=0.02,rely=0.5, relheight=0.46,relwidth=0.96)
    #criação dos botoões do frame
    def _botton_da_tela_frame_01(self):
        #LIMPAR
        self.bt_limpar= Button(self.frame_1,text='LIMPAR', bd= 2, font=('verdana',8,"bold"),command= self.limpar_tela_bt)
        self.bt_limpar.place(relx=0.2,rely=0.1,relwidth=0.1,relheight=0.15, )
        #BUSCAR
        self.bt_buscar= Button(self.frame_1,text='BUSCAR',command= self.buscar_aluno)
        self.bt_buscar.place(relx=0.3,rely=0.1,relwidth=0.1,relheight=0.15)        
        #ALTERAR
        self.bt_alterar= Button(self.frame_1,text='ALTERAR', command=self.alterar_cad)
        self.bt_alterar.place(relx=0.6,rely=0.1,relwidth=0.1,relheight=0.15)
        #LIMPAR
        self.bt_novo = Button(self.frame_1,text='NOVO',command= self.adicionar_aluno)
        self.bt_novo.place(relx=0.7,rely=0.1,relwidth=0.1,relheight=0.15)
        #APAGAR
        self.bt_apagar= Button(self.frame_1,text='APAGAR', bd=2,font=('verdana',8,'bold'),command= self.apagar_cad)
        self.bt_apagar.place(relx=0.8,rely=0.1,relwidth=0.1,relheight=0.15,)
    #caixa de texto da tela da tela superior
    def _label_do_frame_01(self):
        #RA
        self.lb_ra= Label(self.frame_1,text='RA',bg='#F5FFFA')
        self.lb_ra.place(relx=0.04,rely=0.05)
        
        self.ra_entrada = Entry(self.frame_1)
        self.ra_entrada.place(relx=0.04,rely=0.15,relwidth=0.15)
        
        #NOME
        self.lb_nome= Label(self.frame_1,text='Nome do Aluno',bg='#F5FFFA')
        self.lb_nome.place(relx=0.04,rely=0.35)
        
        self.nome_entrada= Entry(self.frame_1)
        self.nome_entrada.place(relx=0.04,rely=0.45,relwidth=0.7)
        
        #Curso
        self.lb_curso= Label(self.frame_1,text='Curso',bg='#F5FFFA')
        self.lb_curso.place(relx=0.04,rely=0.65)
        
        self.curso_entrada= Entry(self.frame_1)
        self.curso_entrada.place(relx=0.04,rely=0.75,relwidth=0.4)
        
        #Telefone
        self.lb_email= Label(self.frame_1,text='E-mail',bg='#F5FFFA')
        self.lb_email.place(relx=0.5,rely=0.6)
        
        self.email_entrada= Entry(self.frame_1)
        self.email_entrada.place(relx=0.50,rely=0.75,relwidth=0.4)
    #treeview - tabela de informações da tela inferior
    def lista_frame_02(self):
        #colunas 
        self.lista_Aluno_Cads =ttk.Treeview(self.frame_2, height=3,columns=("RA","Nome","Curso","E-mail"))
        self.lista_Aluno_Cads.heading('#0',text=" ")
        self.lista_Aluno_Cads.heading('#1',text="RA")
        self.lista_Aluno_Cads.heading('#2',text="Nome do Aluno")
        self.lista_Aluno_Cads.heading('#3',text="Curso")
        self.lista_Aluno_Cads.heading('#4',text="E-mail")
        
        #diemnsionando o tamanho das colunas
        self.lista_Aluno_Cads.column('#0',width=1)
        self.lista_Aluno_Cads.column('#1',width=50)
        self.lista_Aluno_Cads.column('#2',width=125)
        self.lista_Aluno_Cads.column('#3',width=125)
        self.lista_Aluno_Cads.column('#4',width=125)
        
        self.lista_Aluno_Cads.place(relx=0.01,rely=0.1,relwidth=0.95,relheight=0.85)         
        #barra de rolagem
        self.barraderolagem = Scrollbar(self.frame_2, orient='vertical')
        self.lista_Aluno_Cads.configure(yscroll=self.barraderolagem.set)
        self.barraderolagem.place(relx=0.96,rely=0.1,relwidth=0.04,relheight=0.85)
        self.lista_Aluno_Cads.bind("<Double-1>",self.duploclique_apagar)
    #barra de menu superior
    def _menus (self):
       menu_barra =Menu(self.janela)
       self.janela.config(menu=menu_barra)
       filemenu =Menu(menu_barra)
       #filemenu2 =Menu(menu_barra) 
       def _sair(): self.janela.destroy()
       menu_barra.add_cascade(label="Sair",menu=filemenu)
       filemenu.add_command(label="Sair",command=_sair)               
APlicacaoCadastro()