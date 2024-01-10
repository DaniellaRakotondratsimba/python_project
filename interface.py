from dash import Dash, dash_table,html,dcc,Input, Output, State
import TPs as tps

# Initialisation de Dash       
app = Dash(__name__)

# Genère le tableau des documents obtenu avec le mot saisie    
def generate_table(df):
    return (
           dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        tooltip_data=[
            {
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
            } for row in df.to_dict('records')
        ],
    
        # Overflow into ellipsis
        style_cell={
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 0,
            'padding': '1rem',
            "text-align": "center"
        },
        page_size=20,
        tooltip_delay=0,
        tooltip_duration=None
        )
    )


# Affichage de tous les elements
app.title = "Documents"
app.layout = html.Div(children=[
    # Titre
    html.H1(children="Exploration de documents", style={"fontSize": "35px", "color": "black", "text-align": "center"}),
    
    html.Br(),
    html.Div([
        html.Label('Barre de recherche'),
        dcc.Input(id="search", type="text", placeholder="Saisir un/des mot(s)-clé(s)", style= {'margin': '2rem','width':"22%"}),
        html.Button('Rechercher', id='submit-val',n_clicks=0),
        html.Div(id='container-button-basic',
                 children='Entrez une valeur et cliquez sur Rechercher',style={'padding':'1rem 0rem'})     
        ]
        ,style = {"fontSize": "20px",'text-align':'center'}
        
        ),
        
        html.Div('Tahinarisoa Daniella RAKOTONDRATSIMBA & Herinantenainasoa Nancy RANDRIAMIARIJAONA M1 Informatique ',style={"font-weight":"bold","position":'relative', "bottom":0, 
                                                                                "left":0, "right":0, "padding": "1rem", "fontSize": "16px", 
                                                                                "color": "black", "text-align": "center"})
    
    ], style={'padding': '2rem', 'flex': 1},
    )

# Actualisation du mot
@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('search', 'value')
)

# Gère la mise à jour des mots saisies + affiche les elements après la barre de recherche    
def update_output(n_clicks, value):
    
    value = value.lower()
    value = value.split(" ") # séparation des mots clés
    value = list(filter(any, value)) # supprime les espaces inutiles
    
    if len(value) > 0 :  # value is not None          
        tps.DocumentFactory()
        nb_word_dans_doc,top_5_frequence_mot, corpus_value = tps.manipulation_corpus(value)
       
        value = " ou ".join(value)
        return (
                html.Div('{} occurences du mot {} dans les documents '.format(nb_word_dans_doc,value), 
                         style={"text-align":"left"}),
                html.Br(),
                
                html.Div(children=[
                    html.H4(children='Top 5 fréquences ',style={"text-align":"left"}),
                    generate_table(top_5_frequence_mot)]),
                html.Br(),
                
                html.Div(children=[
                    html.H4(children='Contenu du corpus ',style={"text-align":"left"}),
                    generate_table(corpus_value)]),
              ) 
    

 # lance le serveur   
if __name__ == '__main__':
        app.run_server(debug=False)
    
