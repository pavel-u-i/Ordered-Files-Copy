Copyright (C) 2025  Utchev P.I.GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007


Ordered files copy is a Qgis plugin that copies files referenced in layer object attributes, with the option to hierarchically group files into new folders according to other layer object attributes.

The interface is available in two languages: English and Russian. When the plugin is launched, provided that an active layer is present, a window appears for selecting the language and confirming the selection.

Next, you need to select the attribute table field of the active layer that contains links to the location of the files (including photos, etc.) and confirm your selection.

The next step is to interact with the copy type selection interface: with or without grouping, as well as confirming the entry.

When copying without grouping is selected, all files mentioned in the attribute table will be copied to a single folder.

If you choose to copy with grouping, all files mentioned in the attributes table will be copied to different folders created based on the hierarchy specified later.

Also at this stage, if necessary, you should change the type of separator used in attribute cells for multiple file references: the following characters are allowed: ‘;’, ‘,’, ‘|’, ‘\\t’, ‘\\n’.

An additional step is to enter the hierarchy for subsequent file copying. The interface displays all the attribute fields of the active layer. The user must specify at least one parameter, i.e. select the attribute field by which the copied objects will be divided into separate directories: If several parameters are selected, the objects will be divided hierarchically. The position of the parameter in the hierarchy is determined by the order in which it is entered: the first attribute field selected is the main one.

The final stage is interaction with the interface for selecting the destination directory to which the files will be copied. In this case, when copying with grouping, several folders will be created with different positions in the hierarchy, based on the order of listing the attribute fields in the previous stage.


Ordered files copy - это плагин Qgis, который копирует файлы, ссылки на которые содержатся в атрибутах объектов слоя, с возможностью иерархичной группировки файлов в новых папках в соответствии с другими атрибутами объектов слоя.
Интерфейс представлен на двух языка: английский и русский. В момент запуска плагина, с условием наличия активного слоя, появляется соответствующее окно выбора языка и подтверждения выбора.

Далее необходимо выбрать поле таблицы атрибутов активного слоя, в котором содержатся ссылки на расположение файлов (в том числе фотографий и др.) и подтвердить выбор.

Следующим шагом является взаимодействие с интерфейсом выбора типа копирования: с группировкой или без, а также подтверждение ввода.
При выборе копирования без группировки все упоминаемые в таблице атрибутов файлы скопируются в одну папку.
При выборе копирования с группировкой все упоминаемые в таблице атрибутов файлы скопируются в различные папки, создаваемые на основе задаваемой позднее иерархии.
Также на этом этапе, при необходимости, следует изменить тип разделителя, используемого в атрибутивных ячейках для множественной записи ссылок на файлы: допускается использовать следующие символы: ";", ",", "|", "\\t", "\\n".

Дополнительным этапом является ввод иерархии для последующего копирования файлов. Интерфейс отображает все поля атрибутов активного слоя. Пользователю следует задать хотя бы один параметр, то есть выбрать поле атрибутов, по которому будет произведено разделение копируемых объектов на отдельные каталоги: В случае выбора нескольких параметров будет осуществлено иерархичное разделение объектов. Высота положения параметра в иерархии задается последовательностью ввода: первое выбранное поле атрибутов является главным.

Заключительным этапом является взаимодействие с интерфейсом выбора конечного каталога, в который будет выполнено копирование файлов. При этом, в случае копирования с группировкой будет создано несколько папок с различным положением в иерархии, основанным на порядке перечисления полей атрибутов на предыдущем этапе.
