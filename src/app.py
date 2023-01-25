import pandas as pd
import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
#import dash_bootstrap_components as dbc
import dash_table as dt
from flask import Flask
from dash_core_components import Graph
from dash import dash_table

from dash.dash_table.Format import Group
from dash import Dash, dash_table
from func_crea_Graficos import crear_grafico_pie
from func_crea_tablas_simple import create_table_simple
import dash_auth
# import dash_bootstrap_components as dbc
LISTA_USUARIO =[['DIRECCION','A01'],['SUBDIRECCION','A02'],['JESUS','A03'],['JEFEDEPTO','A04']]

meta_tags= [{'name':'viewport',
            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2,minimum-scale=0,5'}]
external_stylesheets=[meta_tags,'assets/css.css','assets/normalize.css']
#https://necolas.github.io/normalize.css/

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#server = Flask(__name__)
auth= dash_auth.BasicAuth(app,LISTA_USUARIO)
server=app.server
# Read data from Excel file
df = pd.read_excel('Plantilla Qna 24.xlsx', sheet_name='Resultados')
df = df.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
df = df[['UM', 'RFC', 'A.Paterno', 'A.Materno', 'Nombre', 'SUELDO TAB', 'CÓDIGO', 'ADSCRIPCION', 'Area Hosp', 'Sub_Area_Hosp', 'NUCLEOS', 'RAMA', 'UNIDAD', 'TURNO', 'EN_PLANTILLA', 'TIPO CONTRATO','NORMATIVA']]


# Define colors for the app
colors = {
    'background': '#621132',
    'background2': '#b38e5d',
    'background3': '#000000',
    'text': '#b38e5d',
    'text1': '#621132',
    'text2': '#ffffff',
    'text3': '#000000',
}
 



#-------------Decorador que da iteractividad al segundo dropdown------------------
@app.callback(
  
    Output('seleccionaUnidades', 'options'),
    Input('seleccionaUnidad', 'value')
)

def set_cities_options(chosen_state):
       if (chosen_state)!= 'JURISDICCIONES':
            dff = df[df['UNIDAD']==(chosen_state)]   
            return [{'label': c, 'value': c} for c in sorted(dff.ADSCRIPCION.unique())]
       elif (chosen_state)== 'JURISDICCIONES':
            dff = df[df['UNIDAD']==(chosen_state)]  
            return [{'label': c, 'value': c} for c in sorted(dff.ADSCRIPCION.unique())]
          
#--------------- Decorador para mostrar una unidad al inicio del programa --------------------
@app.callback(
        Output('seleccionaUnidades', 'value'),
        Input('seleccionaUnidades', 'options')
)
def set_cities_options(chosen_state1):  
        return [k['value']for k in chosen_state1 ][0]

 

 #----------------Decorador grafico por unidad por ramas -----------------------------------------
@app.callback(
    Output(component_id='the_graph1', component_property='figure'),
    
    Input(component_id='seleccionaUnidad', component_property='value')    
    )
def update_graph_pie(my_dropdown):
    return crear_grafico_pie(df, 'UNIDAD', my_dropdown,'numeroRama','RAMA','Distribución Global por Ramas')

    #--------------Decorador grafico por unidad por Turnos -----------------------------------------
@app.callback(
     Output(component_id='the_graphTurnos', component_property='figure'),
     Input(component_id='seleccionaUnidad', component_property='value')      
    )
  
def update_graph_pie(my_dropdown):
    return crear_grafico_pie(df, 'UNIDAD',my_dropdown,'numeroTurno','TURNO','Distribución Global por Turnos')
 
#------------------Decorador grafico por unidad por Ramas -----------------------------------------
@app.callback(
     Output(component_id='theGraphUnidadRamas', component_property='figure'),
    Input(component_id='seleccionaUnidades', component_property='value')      
)

def update_graph_pie(my_dropdown):
    print(my_dropdown)
    return crear_grafico_pie(df,'ADSCRIPCION', my_dropdown, 'numeroRama','RAMA','Distribución por Unidad por Ramas')

#------------------Decorador grafico por unidad por Turnos -----------------------------------------
@app.callback(
     Output(component_id='theGraphUnidadTurnos', component_property='figure'),
    Input(component_id='seleccionaUnidades', component_property='value')      
)

def update_graph_pie(my_dropdown):
    print(my_dropdown)
    return crear_grafico_pie(df,'ADSCRIPCION', my_dropdown, 'numeroTurno','TURNO','Distribución por Unidad por Turnos')


#------------------Decorador tabla unidad rama---------------------
@app.callback(
  Output(component_id='tabla', component_property='data'),
  Input(component_id='seleccionaUnidad', component_property='value')
)
def update_table(seleccionaUnidad):
  dffTabla = df[df['UNIDAD']==(seleccionaUnidad)]
  dffTabla1= dffTabla.groupby(['RAMA']).size().reset_index(name='EN_PLANTILLA')

  # Calcula el total de la columna 'EN_PLANTILLA'
  TOTAL = dffTabla1['EN_PLANTILLA'].sum()

  # Agrega una fila al final de la tabla con el total
  dffTabla1 = dffTabla1.append({'RAMA': 'TOTAL', 'EN_PLANTILLA': TOTAL}, ignore_index=True)

  return dffTabla1.to_dict('records')

#---------------Decorador tabla global turno-----------------
@app.callback(
 Output(component_id='tabla2', component_property='data'),   
Input(component_id='seleccionaUnidad', component_property='value')    
)

def update_table(seleccionaUnidad):
 
      
     dffTabla = df[df['UNIDAD']==(seleccionaUnidad)]
    
     dffTabla2= dffTabla.groupby(['TURNO']).size().reset_index(name='EN_PLANTILLA')
    
     # Calcula el total de la columna 'EN_PLANTILLA'
     TOTAL = dffTabla2['EN_PLANTILLA'].sum()

    # Agrega una fila al final de la tabla con el total
     dffTabla2 = dffTabla2.append({'TURNO': 'TOTAL', 'EN_PLANTILLA': TOTAL}, ignore_index=True)


    
     return dffTabla2.to_dict('records')
   

#------------decorador tabla global rama ----------------
@app.callback(
 Output(component_id='tabla6', component_property='data'),   
 Input(component_id='seleccionaUnidades', component_property='value')    
)

def update_table(seleccionaUnidades):
      
     #dffTabla = df[df['ADSCRIPCION']==(seleccionaUnidades)]
     
     dffTabla3= df.groupby(['UNIDAD']).size().reset_index(name='EN_PLANTILLA')
     
      # Calcula el total de la columna 'EN_PLANTILLA'
     TOTAL = dffTabla3['EN_PLANTILLA'].sum()

    # Agrega una fila al final de la tabla con el total
     dffTabla3 = dffTabla3.append({'UNIDAD': 'TOTAL', 'EN_PLANTILLA': TOTAL}, ignore_index=True)



     return dffTabla3.to_dict('records')
   

#------------decorador tabla por Unidad rama ----------------
@app.callback(
 Output(component_id='tabla3', component_property='data'),   
Input(component_id='seleccionaUnidades', component_property='value')    
)

def update_table(seleccionaUnidades):
 
      
     dffTabla = df[df['ADSCRIPCION']==(seleccionaUnidades)]
     dffTabla3= dffTabla.groupby(['RAMA']).size().reset_index(name='EN_PLANTILLA')
     
      # Calcula el total de la columna 'EN_PLANTILLA'
     TOTAL = dffTabla3['EN_PLANTILLA'].sum()

    # Agrega una fila al final de la tabla con el total
     dffTabla3 = dffTabla3.append({'RAMA': 'TOTAL', 'EN_PLANTILLA': TOTAL}, ignore_index=True)



     return dffTabla3.to_dict('records')
   
#------------Decorador tabla unidad turno ----------------
@app.callback(
 Output(component_id='tabla4', component_property='data'),   
Input(component_id='seleccionaUnidades', component_property='value')    
)

def update_table(seleccionaUnidades):
 
      
     dffTabla = df[df['ADSCRIPCION']==(seleccionaUnidades)]
     dffTabla4= dffTabla.groupby(['TURNO']).size().reset_index(name='EN_PLANTILLA')
     
     # Calcula el total de la columna 'EN_PLANTILLA'
     TOTAL = dffTabla4['EN_PLANTILLA'].sum()

    # Agrega una fila al final de la tabla con el total
     dffTabla4 = dffTabla4.append({'TURNO': 'TOTAL', 'EN_PLANTILLA': TOTAL}, ignore_index=True)

     return dffTabla4.to_dict('records')


#----------------------------------------------------------------------------


#data table
@app.callback(
Output(component_id='table1X', component_property='data'),
Input(component_id='seleccionaUnidades', component_property='value')    
)

def update_table(seleccionaUnidades):
   
    tipo_hospital={
        
        'C0':{'MATUTINA':0, 'VESPERTINA':0, 'VELADA A':0, 'VELADA B':0, 
        'ESPECIAL DIURNA':0, 'ESPECIAL NOCTURNA':0, 'JORNADA ACUMULADA':0,'NO_DEFINIDO':0},

        'C30':{'MATUTINA':72, 'VESPERTINA':29, 'VELADA A':9, 'VELADA B':8, 
        'ESPECIAL DIURNA':10, 'ESPECIAL NOCTURNA':0, 'JORNADA ACUMULADA':0,'NO_DEFINIDO':0},

        'C60':{'MATUTINA':123, 'VESPERTINA':56, 'VELADA A':31, 'VELADA B':29, 
        'ESPECIAL DIURNA':30, 'ESPECIAL NOCTURNA':0, 'JORNADA ACUMULADA':0,'NO_DEFINIDO':0},

        'C90':{'MATUTINA':229, 'VESPERTINA':115, 'VELADA A':60, 'VELADA B':46, 
        'ESPECIAL DIURNA':36, 'ESPECIAL NOCTURNA':1, 'JORNADA ACUMULADA':0,'NO_DEFINIDO':0},

        'C120':{'MATUTINA':269, 'VESPERTINA':144, 'VELADA A':71, 'VELADA B':64, 
        'ESPECIAL DIURNA':44, 'ESPECIAL NOCTURNA':9, 'JORNADA ACUMULADA':0,'NO_DEFINIDO':0},

        }
   
    # Inicializamos dffTabla1x como un DataFrame vacío
    dffTabla1x = pd.DataFrame()
 
    if seleccionaUnidades in ('HOSPITAL GENERAL DE APAN','HOSPITAL GENERAL DE ACTOPAN','HOSPITAL MATERNO INFANTIL','HOSPITAL GENERAL DE HUEJUTLA'):        
            df['NORMATIVA'] = df['TURNO'].apply(lambda x: tipo_hospital['C60'][x] if not pd.isnull(x) else 0)
    elif seleccionaUnidades in ('HOSPITAL GENERAL DE HUICHAPAN', 'HOSPITAL INTEGRAL DE JACALA', 'HOSPITAL ZIMAPAN'):
            df['NORMATIVA'] = df['TURNO'].apply(lambda x: tipo_hospital['C30'][x] if not pd.isnull(x) else 0)
    elif seleccionaUnidades in ('HOSPITAL GENERAL DEL VALLE DEL MEZQUITAL IXMIQUILPAN', 'HOSPITAL GENERAL DE TULA'):
            df['NORMATIVA'] = df['TURNO'].apply(lambda x: tipo_hospital['C90'][x] if not pd.isnull(x) else 0)
    elif seleccionaUnidades == 'HOSPITAL GENERAL TULANCINGO':
            df['NORMATIVA'] = df['TURNO'].apply(lambda x: tipo_hospital['C120'][x] if not pd.isnull(x) else 0)
    else:   df['NORMATIVA'] = df['TURNO'].apply(lambda x: tipo_hospital['C0'][x] if not pd.isnull(x) else 0)
 
    print(df['NORMATIVA'] )  
    dffTabla = df[df['ADSCRIPCION']==(seleccionaUnidades)]
    dffTabla1x= dffTabla.groupby(['ADSCRIPCION','TURNO','NORMATIVA']).size().reset_index(name='EN_PLANTILLA')
    

        # Calcula el total de la columna 'EN_PLANTILLA'
    TOTAL = dffTabla1x['EN_PLANTILLA'].sum()
    TOTAL1= dffTabla1x['NORMATIVA'].sum()
    # Agrega una fila al final de la tabla con el total
    dffTabla1x =  dffTabla1x.append({'ADSCRIPCION': 'TOTAL', 'EN_PLANTILLA': TOTAL,  'NORMATIVA':TOTAL1}, ignore_index=True)

    return dffTabla1x.to_dict('records')
 
 
  #DECORADOR TABLA3
@app.callback(
   
   
    Output(component_id='table3A', component_property='data'),
    
    
    Input('table1X', 'derived_virtual_data'),     
    Input('table1X', 'derived_virtual_selected_rows'),
    Input('table1X', 'selected_rows'),)
     
        
def update_graphs(derived_virtual_data,derived_virtual_selected_rows,selected_rows):
    
    if (selected_rows)is None:
        selected_rows = []
    else:
          
        df=pd.DataFrame(derived_virtual_data)
        df_filterd = df[df.index.isin(selected_rows)]
        return df_filterd.to_dict('records')
   
#DECORADOR TABLA4
@app.callback(
    Output(component_id='table4A', component_property='data'),
   [Input('table3A','data')])
       
def update_graphs(data):
  
    global dataf 
           
    if data !=None:
                
        for dataf in data:
            del dataf['EN_PLANTILLA']                   
                   
            d= df[(df['ADSCRIPCION'] ==dataf['ADSCRIPCION']) &  (df['TURNO'] ==dataf['TURNO']) ]
             
            sjs= pd.DataFrame(d)
            print('gatosb',data)
       
            return sjs.to_dict('records')
       
#----------------------app.layout-------------------------

app.layout= html.Div([
   
        html.Div([
#------------------------ Create marquee--------------------------------------------------
                html.Marquee(id='marquee', children='Prueba rápida VIH, márcate un día y háztela.', style={'color': colors['text2']}),
#-------------------------Create logo-----------------------------------------------------
                html.Img(src='assets/logo.png'),
        ],className='header'),
#---------------------Create header--------------------------------------------------------   
        html.Div([

                html.H1('DIRECCIÓN DE RECURSOS HUMANOS',)
        ],className='header_title'),

       # html.Label('Distribucion Global:', style={'fontSize':20, 'textAlign':'center', 'font-weight': 'bold','color': colors['text']}), 
        html.Label('Distribucion Global:', className='etiqueta'), 
               
#--------------------------tabla globlal secretaria----------------------------        
        html.Div([
            create_table_simple('tabla6', 'UNIDAD', 'UNIDAD'), 
        ]),

        html.Div([
                
                html.Label('Seleccione una Unidad:', className='etiqueta'),
#-------------------Primer Dropdown-----------------------------------------
                dcc.Dropdown(
                id='seleccionaUnidad',
                options=[{'label': s, 'value': s} for s in sorted(df.UNIDAD.unique())],
                value='HOSPITALES',
                clearable=False,
                searchable=False,
                style={'backgroundColor': colors['background2'],'color': colors['text1'], 'font-size': 15, 'font-weight': 'bold'})

        ]),

        html.Div([
                
#------------------- tabla por unidad por ramas----------------------------------
                html.Label('Distribucion de Unidad por Ramas:', className='etiqueta'),
                                
#---------------------grafica ramas--------------------------------------------
                dcc.Graph(id='the_graph1'),                
                        
                create_table_simple('tabla', 'RAMA', 'RAMA'),          
        ]),
            
#-----------------------------------------------------------------------------------------------
                html.Label('Distribucion Global por Turnos:', className='etiqueta'),
#------------------------grafico rama por unidad---------------------------------
                dcc.Graph(id='the_graphTurnos'),

#------------------- tabla por unidad por Turnos----------------------------------
                create_table_simple('tabla2', 'TURNO', 'TURNO'),

        html.Div([
                html.Label('Seleccione una Adscripción:', className='etiqueta'),
                #----------------------Segundo Dropdown--------------------------------------
                dcc.Dropdown(  
                id='seleccionaUnidades',   
                options=[],
                multi=False,
                style={'backgroundColor': colors['background2'],'color': colors['text1'], 'font-size': 15, 'font-weight': 'bold'})        
        ],style={'border-color': '#333', 'border-width': '2px', }),

        html.Div([

                html.Label('Distribucion por Unidad por Rama:', className='etiqueta'),
#-----------------------------------grafico por unidad por ramas------------------------------------------
                dcc.Graph(id='theGraphUnidadRamas'),   
#---------------------------------- tabla Unidades rama  -------------------------------------------------
               
                create_table_simple('tabla3', 'RAMA', 'RAMA'),
                
        ]),

        html.Div([
     
 #--------------------grafico por unidad por ramas------------------------------------------
         
        html.Label('Distribucion por Unidad por Turnos:', className='etiqueta'),
#-----------------------------------grafico por unidad por ramas------------------------------------------       
        dcc.Graph(id='theGraphUnidadTurnos'), 
 #------------------tabla por unidad  turnos-----------------------------------------------
        create_table_simple('tabla4', 'TURNO', 'TURNO'),
        create_table_simple('tabla8', 'Sub_Area_Hosp', 'Sub_Area_Hosp'),

        ]), 

html.Div([
    
html.Label('Comparación de Normativa VS Plantilla:', className='etiqueta'),
 # tabla nucleos
dash_table.DataTable(
        id='table1X',
        #data = dffTabla1.to_dict('records'),
        columns = [{'id':c, 'name':c} for c in 
                   df.loc[:,['ADSCRIPCION','TURNO','EN_PLANTILLA','NORMATIVA']]],
           #virtualization=True,
             row_selectable='multi',
                style_data={
               # 'color':  '#b38e5d',
                'color':  '#ffffff',
                'backgroundColor':'#621132'
            },
            fixed_rows = {'headers':True},

            style_table = {'maxHeight':'450px',
                          'backgroundColor':'#621132',
                         #  'color':  '#b38e5d'},
                           'color':  '#ffffff'},

            style_header = {'backgroundColor':'#000000',
                            'fontWeight':'bold',
                            'border':'4px solid white',
                            'textAlign':'center'},

            style_data_conditional = [
                     {
                'if': {
                    'filter_query': '{EN_PLANTILLA}  > {NORMATIVA}' ,
                    'column_id': 'EN_PLANTILLA'
                },
                'color': 'red',
                'fontWeight': 'bold',
                'textAlign':'center',         
            },
                
                  {
                'if': {
                    'filter_query': '{EN_PLANTILLA}  < {NORMATIVA}' ,
                    'column_id': 'EN_PLANTILLA'
                },
                'color': 'yellow',
                'fontWeight': 'bold',
                 'textAlign':'center',     
            },
                
               {
                'if': {
                    'filter_query': '{EN_PLANTILLA}  = {NORMATIVA}' ,
                    'column_id': 'EN_PLANTILLA'
                },
                'color': 'lime',
               'fontWeight': 'bold',
                'textAlign':'right',   
            },
                {
                'if': {
                    'filter_query': '{NORMATIVA} = {NORMATIVA}',
                    'column_id': 'NORMATIVA'
                },
                'color': 'lime',
               'fontWeight': 'bold',
                'textAlign':'center',   
            }  

              ],

            style_cell = {
                'textAlign':'left',
                'border':'4px solid white',
                 'color':'#b38e5d',
                 
                'maxWidth':'50px',
                # 'whiteSpace':'normal'
                'textOverflow':'ellipsis'


                }),

html.Label('Analítico por Trabajador:', className='etiqueta'),              
# tabla POR PERSONAS
dash_table.DataTable(
        id='table3A',
      
       
        #data=df.to_dict('records'),
        #data = dffTabla1.to_dict('records'),
        columns = [{'id':i, 'name':i, 'deletable':True} for i in 
                   #SI SE LE PONE RFC DESGLOSA UNO A UNO CASO CONTRARIO ACUMULA
                   df.loc[:,['TURNO','EN_PLANTILLA']]],
    
            
       
                style_data={
              
                'color':  '#ffffff',
                'backgroundColor':'#621132'
            },
            fixed_rows = {'headers':True},

            style_table = {'maxHeight':'450px',
                          'backgroundColor':'#621132',
                         #  'color':  '#b38e5d'},
                           'color':  '#ffffff'},

            style_header = {'backgroundColor':'#000000',
                            'fontWeight':'bold',
                            'border':'4px solid white',
                            'textAlign':'center'},

            style_data_conditional = [
                     {
                'if': {
                    'filter_query': '{EN_PLANTILLA}  > {NORMATIVA}' ,
                    'column_id': 'EN_PLANTILLA'
                },
                'color': 'red',
                'fontWeight': 'bold',
                'textAlign':'center',         
            },
                
                  {
                'if': {
                    'filter_query': '{EN_PLANTILLA}  < {NORMATIVA}' ,
                    'column_id': 'EN_PLANTILLA'
                },
                'color': 'yellow',
                'fontWeight': 'bold',
                 'textAlign':'center',     
            },
                
               {
                'if': {
                    'filter_query': '{EN_PLANTILLA}  = {NORMATIVA}' ,
                    'column_id': 'EN_PLANTILLA'
                },
                'color': 'lime',
               'fontWeight': 'bold',
                'textAlign':'right',   
            },
                {
                'if': {
                    'filter_query': '{NORMATIVA} = {NORMATIVA}',
                    'column_id': 'NORMATIVA'
                },
                'color': 'lime',
               'fontWeight': 'bold',
                'textAlign':'center',   
            }  

              ],

            style_cell = {
                'textAlign':'left',
                'border':'4px solid white',
                 'color':'#b38e5d',
                 
                'maxWidth':'50px',
                # 'whiteSpace':'normal'
                'textOverflow':'ellipsis'

                }
),
# Ulitma tabla
dash_table.DataTable(
        id='table4A',
      
     
       
        columns = [{'id':i, 'name':i, 'deletable':True,} for i in 
                   #SI SE LE PONE RFC DESGLOSA UNO A UNO CASO CONTRARIO ACUMULA
                   df.loc[:,['RFC','A.Paterno','A.Materno','Nombre','CÓDIGO','SUELDO TAB','TIPO CONTRATO']]
                     
                   
                   ],
    
        
             

                style_data={
              
                'color':  '#ffffff',
                'backgroundColor':'#621132'
            },
            fixed_rows = {'headers':True},

            style_table = {'maxHeight':'450px',
                          'backgroundColor':'#621132',
                         #  'color':  '#b38e5d'},
                           'color':  '#ffffff',
                            },

            style_header = {'backgroundColor':'#000000',
                            'fontWeight':'bold',
                            'border':'4px solid white',
                            'textAlign':'center'},

            style_data_conditional = [
                     {
                'if': {
                    'filter_query': '{EN_PLANTILLA}  > {NORMATIVA}' ,
                    'column_id': 'EN_PLANTILLA'
                },
                'color': 'red',
                'fontWeight': 'bold',
                'textAlign':'center',         
            },
                
                  {
                'if': {
                    'filter_query': '{EN_PLANTILLA}  < {NORMATIVA}' ,
                    'column_id': 'EN_PLANTILLA'
                },
                'color': 'yellow',
                'fontWeight': 'bold',
                 'textAlign':'center',     
            },
                
               {
                'if': {
                    'filter_query': '{EN_PLANTILLA}  = {NORMATIVA}' ,
                    'column_id': 'EN_PLANTILLA'
                },
                'color': 'lime',
               'fontWeight': 'bold',
                'textAlign':'right',   
            },
                {
                'if': {
                    'filter_query': '{NORMATIVA} = {NORMATIVA}',
                    'column_id': 'NORMATIVA'
                },
                'color': 'lime',
               'fontWeight': 'bold',
                'textAlign':'center',   
            }  

              ],

            style_cell = {
                'textAlign':'left',
                'border':'4px solid white',
                 'color':'#b38e5d',
                 
                #'maxWidth':'5px',
                # 'whiteSpace':'normal'
                'textOverflow':'ellipsis',
                 #'width': 'auto' ,

                }
)

])

],className='contenedor')

df.to_csv('modificado.csv')
if __name__  == '__main__':
       app.run_server(debug=True)