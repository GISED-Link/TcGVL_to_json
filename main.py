# transform variable to 2 json FB's


import tc_sax_reader
import tc_sax_writter
import tc_extract_from_gvl as extractor
import os
import json
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory


CONFIG_FILE_NAME = 'tc_extractor_config.json'


def search_TcGVL_file():
    filename = askopenfilename(filetypes=(("Beckhoff var files", "*.TcGVL"), ("All files", "*.*")))
    ent1.delete(0, tk.END)
    ent1.insert(tk.END, filename)  # add this
    prj_config['file_to_extract'] = filename


def search_project_path():
    dir_name = askdirectory()
    ent2.delete(0, tk.END)
    ent2.insert(tk.END, dir_name)  # add this
    prj_config['project_path'] = dir_name


def load_config():
    config = {'project_path': os.path.dirname(os.path.realpath(__file__)), 'file_to_extract': ''}
    config_file_path = os.path.dirname(os.path.realpath(__file__)) + '\\' + CONFIG_FILE_NAME

    try:
        config_file = open(config_file_path, 'r')
        config = json.loads(config_file.read())
        config_file.close()
    except IOError:
        config_file = open(config_file_path, 'w')
        config_file.write(json.dumps(config))
        print('a new configuration file has been created')
        config_file.close()

    return config


def save_config(config):
    config_file_path = os.path.dirname(os.path.realpath(__file__)) + '\\' + CONFIG_FILE_NAME
    try:
        config_file = open(config_file_path, 'w')
        config_file.write(json.dumps(config))
        config_file.close()
    except IOError:
        print('unable to save the file properly')


def generate():
    variable_to_parse, namesapce = extractor.extract_token_from_file(prj_config['file_to_extract'], prj_config['project_path'] + '/')
    writer_st, writer_var = tc_sax_writter.parse_writer(variable_to_parse, namesapce + '.')
    reader_st, reader_var = tc_sax_reader.parse_reader(variable_to_parse, namesapce + '.')

    var_reader.delete('1.0', tk.END)
    var_reader.insert(tk.END, writer_var)

    st_reader.delete('1.0', tk.END)
    st_reader.insert(tk.END, writer_st)

    var_writer.delete('1.0', tk.END)
    var_writer.insert(tk.END, reader_var)

    st_writer.delete('1.0', tk.END)
    st_writer.insert(tk.END, reader_st)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    prj_config = load_config()
    
    root = tk.Tk()
    root.title('tc json st code generator')
    root.geometry("800x600")
    root.columnconfigure(3, weight=1)
    root.columnconfigure(4, weight=0)
    root.columnconfigure(5, weight=1)
    root.columnconfigure(6, weight=0)
    root.rowconfigure(8, weight=3)
    root.rowconfigure(10, weight=1)

    label1 = tk.Label(root, font=40, text='TcGVL file:')
    label1.grid(row=2, column=1)

    ent1 = tk.Entry(root, font=40)
    ent1.insert(0, prj_config['file_to_extract'])
    ent1.grid(row=2, column=3, sticky='EW', columnspan=4)

    b1 = tk.Button(root, text="Search", font=40, width=10, bg='light blue', command=search_TcGVL_file)
    b1.grid(row=2, column=7, sticky='EW', columnspan=2)

    label2 = tk.Label(root, font=40, text='Project path:')
    label2.grid(row=4, column=1)

    ent2 = tk.Entry(root, font=40)
    ent2.insert(0, prj_config['project_path'])
    ent2.grid(row=4, column=3, sticky='EW', columnspan=4)

    b2 = tk.Button(root, text="Search", font=40, width=10, bg='light blue', command=search_project_path)
    b2.grid(row=4, column=7, sticky='EW', columnspan=2)

    b3 = tk.Button(root, text="Generate", font=40, width=10, bg='light green', command=generate)
    b3.grid(row=5, column=7, sticky='EW', columnspan=2)

    var_reader_sb = tk.Scrollbar(root)
    var_reader_sb.grid(row=8, column=4, sticky='NS')
    var_reader = tk.Text(root, font=18, state=tk.NORMAL, yscrollcommand=var_reader_sb.set)
    var_reader.grid(row=8, column=1, sticky='EW', columnspan=3)

    st_reader_sb = tk.Scrollbar(root)
    st_reader_sb.grid(row=10, column=4, sticky='NS')
    st_reader = tk.Text(root, font=18, state=tk.NORMAL, yscrollcommand=st_reader_sb.set)
    st_reader.grid(row=10, column=1, sticky='EW', columnspan=3)

    var_writer_sb = tk.Scrollbar(root)
    var_writer_sb.grid(row=8, column=8, sticky='NS')
    var_writer = tk.Text(root, font=18, state=tk.NORMAL, yscrollcommand=var_writer_sb.set)
    var_writer.grid(row=8, column=5, sticky='EW', columnspan=3)

    st_writer_sb = tk.Scrollbar(root)
    st_writer_sb.grid(row=10, column=8, sticky='NS')
    st_writer = tk.Text(root, font=18, state=tk.NORMAL, yscrollcommand=st_writer_sb.set)
    st_writer.grid(row=10, column=5, sticky='EW', columnspan=3)

    root.mainloop()

    save_config(prj_config)
