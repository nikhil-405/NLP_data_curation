#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# Spanish bad words stored in a set for fast lookup
bad_words = {
    'mierda', 'puta', 'cabron', 'imbecil', 'estupido', 'gilipollas', 'pendejo', 'idiota',
    'cojones', 'coño', 'chingar', 'joder', 'cabrón', 'hijo de puta', 'zorra', 'culero',
    'marica', 'pendeja', 'puto', 'polla', 'pito', 'verga', 'pajero', 'cogido', 'cogiendo',
    'maldito', 'malparido', 'bastardo', 'chinga', 'chingada', 'chingado', 'pendejada',
    'tarado', 'baboso', 'asqueroso', 'cabrona', 'putona', 'pelotudo', 'boludo', 'mamón',
    'pinche', 'culiao', 'carajo', 'infeliz', 'huevón', 'lameculos', 'cagón', 'chupapollas',
    'puta madre', 'perra', 'capullo', 'cojudo', 'maricón', 'tragaleche', 'cornudo',
    'me cago', 'mierdero', 'cagada', 'chupamela', 'chingón', 'culón', 'culera',
    'hijueputa', 'gonorrea', 'follando', 'cabronazo', 'culear', 'maricona', 'culiado',
    'vergon', 'tragasables', 'chupacabras', 'coñazo', 'jilipollas', 'cogetudo',
    'putazo', 'gilipolla', 'meapilas', 'cabronada', 'malparida', 'tarada', 'babosa',
    'cabroncillo', 'mamonazo', 'cagao', 'chingadazo', 'pelotuda', 'boluda', 'culon',
    'culiada', 'hijo de perra', 'huevona', 'chupame', 'lameculo', 'cagon',
    'chingada madre', 'pajera', 'huevon', 'boluda', 'coñazo', 'mamón', 'cagada'
}

def check_file_for_bad_words(file_path, bad_words):
    with open(file_path, 'r') as file:
        content = file.read().lower()  
        if bad_word in content:
            return True
    return False

def delete_bad_word_file(file_path):
    os.remove(file_path)
    print(f"Deleted: {file_path}")

def check_folder_and_delete_bad_files(folder_path, bad_words):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):  
            file_path = os.path.join(folder_path, filename)
            if check_file_for_bad_words(file_path, bad_words): 
                delete_bad_word_file(file_path)  

# Example usage
def main():
    folder_path = '/home/spanish_nlp/NLP_Assignment_1/wikipedia/wikipedia_scraper/articles'  # Change this to your folder path

    
    check_folder_and_delete_bad_files(folder_path, bad_words)

    print("Processing complete.")

if __name__ == "__main__":
    main()