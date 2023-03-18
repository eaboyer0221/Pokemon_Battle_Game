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


class PokemonGame:
    def __init__(self):
        self.df = self.pokedex()
        # main window of game
        self.root = tk.Tk()
        self.root.title("Pokedex")

        ##### Middle Pokedex Section #######
        self.pokemon_selection = Label(self.root, text="Pokemon Selection", bg="lightgrey")
        self.pokemon_selection.grid(row=0, column=1, columnspan=4, padx=5, pady=5)

        # Type Selection dropdown menu
        # Label for Type Selection
        ttk.Label(self.root, text="Type:",
                  font=("Times New Roman", 10)).grid(column=1,
                                                     row=1, padx=1, pady=2)
        self.n = tk.StringVar()
        self.type_selection = ttk.Combobox(self.root, width=10,
                                      textvariable=self.n)

        # Adding combobox drop down list
        self.type_selection['values'] = (' -All-',
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

        self.type_selection.grid(column=2, row=1)

        # Shows -All- as a default value
        self.type_selection.current(0)
        # Adding trace to the combobox
        self.n.trace('w', lambda *args: self.filter_table())

        # Search box for Pokemon
        ttk.Label(self.root, text="Name:",
                  font=("Times New Roman", 10)).grid(column=3,
                                                     row=1, padx=10, pady=2)
        self.name_text = tk.StringVar()
        self.name = tk.Entry(self.root, width=20, textvariable=self.name_text)
        self.name.grid(column=4, row=1, padx=1, pady=2)
        self.name_text.trace('w', lambda *args: self.filter_table())

        ###Pokedex Table###
        # create a frame for the pokedex table with a horizontal scrollbar
        self.table_frame = tk.Frame(self.root)
        self.table_frame.grid(row=2, column=1, columnspan=4, rowspan=2, padx=1, pady=1)

        self.xscrollbar = tk.Scrollbar(self.table_frame, orient='horizontal')
        self.xscrollbar.pack(side='bottom', fill='x')

        # create the tkinter window and table
        self.tree = ttk.Treeview(self.table_frame, xscrollcommand=self.xscrollbar.set, show='headings')

        self.tree['columns'] = self.df.columns

        # create a dictionary to map column names to column indices
        self.column_dict = {col: i for i, col in enumerate(self.df.columns)}

        # add the pokedex columns to the Treeview widget
        for col in self.df.columns:
            self.tree.column(self.column_dict[col], width=80, stretch=True)
            self.tree.heading(self.column_dict[col], text=col)
        # configure the scrollbar to scroll the treeview widget
        self.xscrollbar.config(command=self.tree.xview)
        self.tree.pack(side='left')
        # set padx=0 to remove horizontal padding
        self.table_frame.grid_columnconfigure(0, weight=1, pad=0)
        self.filter_table()

        # Select Button
        Button(self.root, text="Select", command=lambda: self.show_pokemon_info()).grid(row=4, column=1, columnspan=3)

        self.root.mainloop()

    #create pokedex dataframe
    def pokedex(self, url = 'https://pokemondb.net/pokedex/all'):
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


    #create function to filter pokedex table based on search
    def filter_table(self):
        selected_type = self.type_selection.get()
        print(selected_type)
        search_text = self.name_text.get()

        if selected_type == ' -All-':
            filtered_df = self.df
        else:
            filtered_df = self.df[self.df['Type'].str.contains(selected_type)]
        search_df = self.df
        if search_text:
            search_df = self.df[self.df['Name'].str.startswith(search_text, na=False)]

        #search_df = self.df[self.df['Name'].str.startswith(search_text, na=False)]
        self.tree.delete(*self.tree.get_children())

        for i, row in pd.merge(filtered_df, search_df, how='inner', on=['Number']).iterrows():
            self.tree.insert('', 'end',values=tuple(row))
    def show_pokemon_info(self):
        # Get the selected Pokemon from the Treeview widget
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])  # Get the first selected item
            values = item['values']  # Get the values of the selected item
            pokemon = self.df.loc[self.df['Name'] == values[1]]  # Get the row of the selected Pokemon from the dataframe

            # Create a new window to display the Pokemon info
            info_window = tk.Toplevel(self.root)
            info_window.title("Pokemon Info")

            # Add labels and values to display the Pokemon info
            tk.Label(info_window, text="Name:").grid(row=0, column=0)
            tk.Label(info_window, text=pokemon['Name'].values[0]).grid(row=0, column=1)
            tk.Label(info_window, text="Type:").grid(row=1, column=0)
            tk.Label(info_window, text=pokemon['Type'].values[0]).grid(row=1, column=1)
            tk.Label(info_window, text="HP:").grid(row=2, column=0)
            tk.Label(info_window, text=pokemon['HP'].values[0]).grid(row=2, column=1)
            tk.Label(info_window, text="Attack:").grid(row=3, column=0)
            tk.Label(info_window, text=pokemon['Attack'].values[0]).grid(row=3, column=1)
            tk.Label(info_window, text="Defense:").grid(row=4, column=0)
            tk.Label(info_window, text=pokemon['Defense'].values[0]).grid(row=4, column=1)

            # Add an image of the Pokemon to the window
            response = requests.get(pokemon['image_url'].values[0])
            img = Image.open(io.BytesIO(response.content))
            img = img.resize((100, 100))
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(info_window, image=img)
            img_label.image = img
            img_label.grid(row=0, column=2, rowspan=5, padx=10)

            # Make the window stay open until the user closes it
            info_window.mainloop()
        else:
            # If no Pokemon is selected, show an error message
            tk.messagebox.showerror("Error", "Please select a Pokemon from the table.")


if __name__ == "__main__":
    PokemonGame()



