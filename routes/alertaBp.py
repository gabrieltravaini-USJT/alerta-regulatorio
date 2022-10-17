from flask import Blueprint, render_template, request, redirect, url_for
from..extensions import base_alerta
from..models.base import Alerta
import pandas as pd
from datetime import date, datetime
from sqlalchemy import desc

#instanciar a blueprint do site
alertaBp = Blueprint('alertaBp',__name__)


#declaração de rotas (paginas) do site

@alertaBp.route('/populate')
def testebanco():
    
    base_alerta.create_all()
    df_data = {'id' : [1,2,3,4,5,6,7,8,9,10], 
               'titulo':["alerta1","alerta2","alerta3","alerta4","alerta5","alerta6","alerta7","alerta8","alerta9","alerta10"],
               'resumo':["Lorem ipsum dolor sit amet, consectetur adipiscing elit", "Lorem ipsum dolor sit amet, consectetur adipiscing elit", "Lorem ipsum dolor sit amet, consectetur adipiscing elit", "Lorem ipsum dolor sit amet, consectetur adipiscing elit", "Lorem ipsum dolor sit amet, consectetur adipiscing elit", "Lorem ipsum dolor sit amet, consectetur adipiscing elit", "Lorem ipsum dolor sit amet, consectetur adipiscing elit", "Lorem ipsum dolor sit amet, consectetur adipiscing elit", "Lorem ipsum dolor sit amet, consectetur adipiscing elit", "Lorem ipsum dolor sit amet, consectetur adipiscing elit"],
               'link':["www.link.com","www.link.com","www.link.com","www.link.com","www.link.com","www.link.com","www.link.com","www.link.com","www.link.com","www.link.com"],
               'fonte':['BACEN','BACEN','BACEN','SUSEP','ANS','ANS','SUSEP','ANS',"SUSEP","ANS"],
               'data':[date(2022,10,2),date(2022,10,3),date(2022,10,4),date(2022,4,1),date(2022,9,14),date(2022,6,5),date(2021,3,4),date(2022,9,20),date(2022,7,10),date(2022,1,2)],
               'pldft':[False,False,True,False,False,False,True,False,False,False,]}
    df_teste = pd.DataFrame(data=df_data)

    for index, row in df_teste.iterrows():
        alerta = Alerta(id = row.id, titulo = row.titulo, resumo = row.resumo, link = row.link, fonte = row.fonte, data = row.data, pldft = row.pldft)
        base_alerta.session.add(alerta)
    base_alerta.session.commit()
    
    return redirect(url_for('alertaBp.home'))
    

@alertaBp.route('/')
def home():
    lista = Alerta.query.order_by(desc(Alerta.data)).all()
    datahoje = datetime.strftime(date.today(),"%Y-%m-%d")
    return render_template('home.html',alerta = lista, hoje = datahoje)


@alertaBp.route('/filter',methods = ["POST"])
def filter ():

    buscaID = request.form['buscaID']
    if buscaID == "digite o ID para Buscar" or buscaID =="":
        buscaID = 0
    else:
        buscaID = int(buscaID)
    buscaorigem = [False,False,False]
    if request.form.get('FonteSUSEP'):
        buscaorigem[0] = True
    if request.form.get ("FonteANS"):
        buscaorigem[1] = True
    if request.form.get('FonteBACEN'):
        buscaorigem[2] = True
    dataini = datetime.strptime(request.form["inicio"], '%Y-%m-%d')
    datafim = datetime.strptime(request.form["fim"], '%Y-%m-%d')
    filtropldft = True if request.form.get ('FiltroPLDFT') else False

    print(buscaID)
    print(buscaorigem)
    print(dataini)
    print(datafim)
    print(filtropldft)
    começobusca = date(1,1,1)
    if buscaID == 0 and buscaorigem[0] == True and buscaorigem[1]== True and buscaorigem[2]==True and filtropldft==False and dataini ==começobusca and datafim == date.today() :
        print("passa tudo")
        lista = Alerta.query.order_by(desc(Alerta.data)).all()
    elif (buscaID!=0):
        lista = Alerta.query.filter_by(id = buscaID).all()
        print("passa busca direta")  
    else:
        print("passa filtro")
        listaorigem = []
        if buscaorigem[0]==True:
            listaorigem.append(Alerta.query.filter_by(fonte = 'SUSEP').all())
        if buscaorigem[1]==True:
            listaorigem.append(Alerta.query.filter_by(fonte = 'ANS').all())
        if buscaorigem[2]==True:
            listaorigem.append(Alerta.query.filter_by(fonte = 'BACEN').all())
        
        listaorigem = flatten(listaorigem)

        
        listadata = Alerta.query.filter(Alerta.data.between(dataini,datafim)).all()
    

        listaorigem_e_data = intersection(listaorigem,listadata)
    

        if filtropldft == True:
            listapldft =Alerta.query.filter_by(pldft = True).all()
            lista = intersection(listaorigem_e_data,listapldft)
        else:
            lista = listaorigem_e_data    
        
    
    dataini = datetime.strftime(dataini,"%Y-%m-%d")
    datafim = datetime.strftime(datafim,"%Y-%m-%d")
    if len(lista)>0:

        if buscaID == 0:
            buscaID = "digite o ID para Buscar"
        return render_template('filter.html',alerta=lista, bid=buscaID, borigem0 = str(buscaorigem[0]), borigem1=str(buscaorigem[1]),borigem2=str(buscaorigem[2]),dini=dataini,dfim =datafim,pldft=str(filtropldft))
    else:
        return "Resultado vazio, retorne à home"






def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

def flatten(lst):
    return [item for sublist in lst for item in sublist]