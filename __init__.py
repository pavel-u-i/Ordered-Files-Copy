# Copyright (C) 2025  Utchev P.I.GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

def classFactory(iface):
    from .ordered_files_copy import OrderedFilesCopyPlugin
    return OrderedFilesCopyPlugin(iface)
