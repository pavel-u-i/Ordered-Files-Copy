Ordered files copy

If the QGIS plugin ‘Ordered files copy’ proves useful for your research or work, please cite our article. This will help us support our work and allow us to continue developing and maintaining the plugin. For your convenience, here is the link:
Utchev, P. I. (2025). Ordered files copy - Qgis Plugin. Zenodo. https://doi.org/10.5281/zenodo.17093201

Ordered files copy is a Qgis plugin that copies files referenced in layer object attributes, with the option to hierarchically group files into new folders according to other layer object attributes.
The interface is available in two languages: English and Russian. When the plugin is launched, provided that an active layer is present, a window appears for selecting the language and confirming the selection.

Next, select the attribute table field of the active layer that contains links to the location of files (including photos, etc.) and confirm your selection.

The next step is to interact with the copy type selection interface: with or without grouping, as well as confirming the input.
When selecting copying without grouping, all files mentioned in the attributes table will be copied to a single folder.
If you select copying with grouping, all files mentioned in the attributes table will be copied to different folders created based on the hierarchy specified later.
Also at this stage, if necessary, you should change the type of separator used in the attribute cells for multiple file references: the following characters are allowed: ‘;’, ‘,’, ‘|’, ‘\\t’, ‘\\n’.

An additional step is to enter the hierarchy for subsequent file copying. The interface displays all the attribute fields of the active layer. The user must specify at least one parameter, i.e. select the attribute field by which the copied objects will be divided into separate directories: If several parameters are selected, the objects will be divided hierarchically. The position of the parameter in the hierarchy is determined by the order in which it is entered: the first attribute field selected is the main one.

The final stage involves interacting with the interface for selecting the destination directory to which the files will be copied. In this case, if copying with grouping, several folders will be created with different positions in the hierarchy based on the order of the attribute fields listed in the previous stage.
