import io
import tkinter as tk
from tkinter import *
from tkinter import ttk
import random
import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import requests


#create pokedex dataframe
def pokedex(url = 'https://pokemondb.net/pokedex/all'):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'pokedex'})
    headers = []
    for th in table.find('thead').find_all('th'):
        headers.append(th.text.strip())
    headers.append('image_url')
    rows = []
    for tr in table.find('tbody').find_all('tr'):
        row = []
        for td in tr.find_all('td'):
            row.append(td.text.strip())
        row.append(tr.find("img")['src'])
        rows.append(row)
    df = pd.DataFrame(rows, columns=headers)
    df = df.rename(columns={'#':'Number', 'Sp. Atk':'Special_Attack', 'Sp. Def':'Special_Defense'})
    return df

df = pokedex()


#main window of game
root = tk.Tk()
root.title("Pokemon Battle")


##### Middle Pokedex Section #######
# Enter specific information for your profile into the following widgets
pokemon_selection = Label(root, text="Pokemon Selection", bg="lightgrey")
pokemon_selection.grid(row=0, column=1, columnspan=4, padx=5, pady=5)

#Type Selection dropdown menu
# Label for Type Selection
ttk.Label(root, text="Type:",
          font=("Times New Roman", 10)).grid(column=1,
                                             row=1, padx=1, pady=2)
n = tk.StringVar()
type_selection = ttk.Combobox(root, width=10,
                            textvariable=n)

# Adding combobox drop down list
type_selection['values'] = (' -All-',
                          ' Normal',
                          ' Fire',
                          ' Water',
                          ' Electric',
                          ' Grass',
                          ' Ice',
                          ' Fighting',
                          ' Poison',
                          ' Ground',
                          ' Flying',
                          ' Psychic',
                          'Bug',
                          'Rock',
                          'Ghost',
                          'Dragon',
                          'Dark',
                          'Steel',
                          'Fairy'
                          )

type_selection.grid(column=2, row=1)

# Shows -All- as a default value
type_selection.current(0)


#Search box for Pokemon

ttk.Label(root, text="Name:",
          font=("Times New Roman", 10)).grid(column=3,
                                             row=1, padx=10, pady=2)
name_text = tk.StringVar()
name = tk.Entry(root, width=20, textvariable=name_text)
name.grid(column=4, row=1, padx=1, pady=2)
name_text.trace('w', lambda *args: filter_table())


###Pokedex Table###

# create a frame for the pokedex table with a horizontal scrollbar
table_frame = tk.Frame(root)
table_frame.grid(row=2, column=1, columnspan=4, rowspan=2, padx=1, pady=1)

xscrollbar = tk.Scrollbar(table_frame, orient='horizontal')
xscrollbar.pack(side='bottom', fill='x')

# create the tkinter window and table
tree = ttk.Treeview(table_frame, xscrollcommand=xscrollbar.set, show='headings')

tree['columns'] = df.columns

# create a dictionary to map column names to column indices
column_dict = {col: i for i, col in enumerate(df.columns)}


#add the pokedex columns to the Treeview widget
for col in df.columns:
    tree.column(column_dict[col], width=80, stretch=True)
    tree.heading(column_dict[col], text=col)

#create function to filter pokedex table based on search
def filter_table():
    selected_type = type_selection.get()
    print(selected_type)
    search_text = name_text.get()
    df = pokedex()

    if selected_type == ' -All-':
        filtered_df = df
    else:
        filtered_df = df[df['Type'].str.contains(selected_type)]
    search_df = df[df['Name'].str.startswith(search_text, na=False)]
    tree.delete(*tree.get_children())
    for i, row in filtered_df.iterrows():
        tree.insert('', 'end',values=tuple(row))
    df = filtered_df
    load_table()
# text=str(i),
#add the rows to the Treeview widget
def load_table():
    for i, row in df.iterrows():
        tree.insert('', 'end', values=tuple(row))


#text=str(i),
# configure the scrollbar to scroll the treeview widget
xscrollbar.config(command=tree.xview)
tree.pack(side='left')
# set padx=0 to remove horizontal padding
table_frame.grid_columnconfigure(0, weight=1, pad=0)
filter_table()


#Battle Button
Button(root, text="Battle").grid(row=4, column=1, columnspan=3)



root.mainloop()




