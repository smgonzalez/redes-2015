#!/usr/bin/python

import argparse
import os

DEFAULT_DOT_FILE='graph.dot'

SRC_INDEX=3
DST_INDEX=4
TYPE_INDEX=5

DOT_FILE_BEGIN="digraph graf {\nnode [fontsize=30, labelfontsize= 25, shape=ellipse, width=3.0, height=1.5]\n"
DOT_FILE_END="}"

DOT_WHO_HAS_VERTEX_FORMAT= '"%s" -> "%s" [label="%d REQ  "];\n'
DOT_IS_AT_VERTEX_FORMAT= '"%s" -> "%s" [style=dotted, label="%d REP  "];\n'

WHO_HAS="ARP:who-has"
IS_AT="ARP:is-at"

DOT_COMMAND="dot -Tjpg %s -o %s" # dot_file, img_file
VIEW_COMMAND="xdg-open %s" # img_file

class Graficador(object):
    
    def __init__(self, data_file, dot_file, out_file):
        self.data = data_file
        self.dot_file = dot_file
        self.img = out_file

    def graficar(self):

        print("Generando archivo dot: ", self.dot_file.name)
        self.parse_data_file()
        
        self.dot_file.write(DOT_FILE_BEGIN)

        for (src,dst), quantity in self.who_has_dict.items():
            vertex = DOT_WHO_HAS_VERTEX_FORMAT % (src, dst, quantity)
            self.dot_file.write(vertex)

        for (src,dst), quantity in self.is_at_dict.items():
            vertex = DOT_IS_AT_VERTEX_FORMAT % (src, dst, quantity)
            self.dot_file.write(vertex)


        self.dot_file.write(DOT_FILE_END)
        self.dot_file.close()

        print("Archivo ", self.dot_file.name, " generado")
        print("Graficando ....")
        os.system(DOT_COMMAND % (self.dot_file.name, self.img.name))
        print("Grafico generado en: ", self.img.name)
        os.remove(self.dot_file.name)
        print("Abriendo imagen ....")
        os.system(VIEW_COMMAND % self.img.name)



    def parse_data_file(self):

        self.who_has_dict = {}
        self.is_at_dict = {}

        next(self.data)

        for line in self.data:
            packet = line.split()
            source = packet[SRC_INDEX]
            dest = packet[DST_INDEX]
            ptype = packet[TYPE_INDEX]
            if ptype not in [WHO_HAS,IS_AT]:
                continue
            
            arp_dict = self.who_has_dict if ptype==WHO_HAS else self.is_at_dict

            if arp_dict.get((source,dest)) != None:
                arp_dict[(source,dest)] += 1
            else:
                arp_dict[(source,dest)] = 1
        
        self.data.close()


if __name__ == '__main__':

    args_parser = args_parser = argparse.ArgumentParser(description='Graficador de grafos')
    args_parser.add_argument('data', type=argparse.FileType('r'), metavar='ARCHIVO_DATOS', help='Archivo de entrada')
    args_parser.add_argument('-d', dest='dot_file', type=argparse.FileType('w'), default=DEFAULT_DOT_FILE, metavar='ARCHIVO_DOT', help='Nombre de archivo para DOT')
    args_parser.add_argument('out_file', type=argparse.FileType('w'), default='graph.jpg', metavar='NOMBRE_IMAGEN', help='Imagen de salida')

    params = vars(args_parser.parse_args())

    data_file = params['data']
    dot_file = params['dot_file']
    out_file = params['out_file']

    graficador = Graficador(data_file, dot_file, out_file)

    graficador.graficar()



