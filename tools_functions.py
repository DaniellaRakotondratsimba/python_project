import pandas as pd

# lecture d'un CSV
def load_data(path_file :str):
      return pd.read_csv(path_file,sep=';')
  
    
  
