# Copyright (C) 2025  Utchev P.I. GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007




import os
import shutil
import re
from qgis.core import QgsProject
from qgis.PyQt.QtWidgets import (QFileDialog, QInputDialog, QDialog, 
                                 QVBoxLayout, QListWidget, QListWidgetItem,
                                 QDialogButtonBox, QLabel, QPushButton, 
                                 QHBoxLayout, QAction, QMessageBox,
                                 QRadioButton, QButtonGroup, QGroupBox,
                                 QComboBox)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import Qt
from qgis.gui import QgisInterface
from qgis.utils import iface

from .resources import *

class OrderedFilesCopyPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.current_language = "ru"  # язык по умолчанию
        
        # Локальный русско-английский словарь
        self.translations = {
            "ru": {
                "plugin_name": "Ordered Files Copy",
                "menu_tools": "&Инструменты",
                "error_no_layer": "Нет активного слоя!",
                "mode_selection": "Выбор режима работы",
                "mode_group": "Режим работы:",
                "mode_with_grouping": "С группировкой по атрибутам",
                "mode_without_grouping": "Без группировки (все файлы в одну папку)",
                "multi_file_settings": "Настройки нескольких файлов:",
                "separator_label": "Разделитель для нескольких файлов в одном атрибуте:",
                "separator_prompt": "Введите разделитель для нескольких файлов:",
                "select_field": "Выбор поля",
                "select_field_prompt": "Выберите поле с путями к файлам:",
                "choose_folder": "Выберите папку для сохранения всех файлов",
                "choose_root_folder": "Выберите корневую папку для сохранения",
                "done": "Готово",
                "copied_files": "Скопировано файлов:",
                "errors": "Ошибок:",
                "multi_file_objects": "Объектов с несколькими файлами:",
                "hierarchical_folders": "Создано иерархических папок:",
                "error_no_grouping_fields": "Не выбраны поля для группировки!",
                "field_order_selection": "Выбор порядка полей для группировки",
                "field_order_instruction": "Выберите поля в порядке важности (первое - самый высокий уровень):",
                "available_fields": "Доступные поля:",
                "grouping_order": "Порядок группировки (сверху - высший уровень):",
                "add_button": "→ Добавить",
                "remove_button": "← Удалить",
                "move_up": "↑ Вверх",
                "move_down": "↓ Вниз",
                "language_settings": "Настройки языка:",
                "select_language": "Выберите язык интерфейса:"
            },
            "en": {
                "plugin_name": "Ordered Files Copy",
                "menu_tools": "&Tools",
                "error_no_layer": "No active layer!",
                "mode_selection": "Mode Selection",
                "mode_group": "Operation mode:",
                "mode_with_grouping": "With attribute grouping",
                "mode_without_grouping": "Without grouping (all files in one folder)",
                "multi_file_settings": "Multiple files settings:",
                "separator_label": "Separator for multiple files in one attribute:",
                "separator_prompt": "Enter separator for multiple files:",
                "select_field": "Field Selection",
                "select_field_prompt": "Select field with file paths:",
                "choose_folder": "Choose folder to save all files",
                "choose_root_folder": "Choose root folder for saving",
                "done": "Done",
                "copied_files": "Copied files:",
                "errors": "Errors:",
                "multi_file_objects": "Objects with multiple files:",
                "hierarchical_folders": "Hierarchical folders created:",
                "error_no_grouping_fields": "No grouping fields selected!",
                "field_order_selection": "Field Order Selection",
                "field_order_instruction": "Select fields in order of importance (first - highest level):",
                "available_fields": "Available fields:",
                "grouping_order": "Grouping order (top - highest level):",
                "add_button": "→ Add",
                "remove_button": "← Remove",
                "move_up": "↑ Up",
                "move_down": "↓ Down",
                "language_settings": "Language settings:",
                "select_language": "Select interface language:"
            }
        }
        
    def tr(self, key):
        """Возвращает перевод для текущего языка"""
        return self.translations[self.current_language].get(key, key)
        
    def initGui(self):
        qInitResources()
        icon = QIcon(":/plugins/Ordered files copy/icon.png")
        
        #ИКОНКА            
        self.action = QAction(
            icon,
            self.tr("plugin_name"),
            self.iface.mainWindow()
        )
        self.action.triggered.connect(self.run)
        
        # Добавляем в меню и панель инструментов
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(self.tr("menu_tools"), self.action)
        
    def unload(self):
        # Удаляем из меню и панели инструментов
        self.iface.removePluginMenu(self.tr("menu_tools"), self.action)
        self.iface.removeToolBarIcon(self.action)
        qCleanupResources()
    
    def run(self):
        """Основная функция запуска плагина"""
        # Сначала показываем диалог выбора языка
        self.show_language_selection_dialog()
    
    def show_language_selection_dialog(self):
        """Диалог выбора языка интерфейса"""
        class LanguageSelectionDialog(QDialog):
            def __init__(self, plugin, parent=None):
                super().__init__(parent)
                self.plugin = plugin
                self.setWindowTitle("Language Selection / Выбор языка")
                self.setMinimumWidth(300)
                
                layout = QVBoxLayout()
                
                # Выбор языка
                layout.addWidget(QLabel("Select language / Выберите язык:"))
                self.language_combo = QComboBox()
                self.language_combo.addItem("Русский (Russian)", "ru")
                self.language_combo.addItem("English (Английский)", "en")
                
                # Устанавливаем текущий язык
                current_index = self.language_combo.findData(self.plugin.current_language)
                if current_index >= 0:
                    self.language_combo.setCurrentIndex(current_index)
                
                layout.addWidget(self.language_combo)
                
                # Кнопки OK/Cancel
                buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
                buttons.accepted.connect(self.accept)
                buttons.rejected.connect(self.reject)
                layout.addWidget(buttons)
                
                self.setLayout(layout)
            
            def get_selected_language(self):
                return self.language_combo.currentData()
        
        dialog = LanguageSelectionDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.current_language = dialog.get_selected_language()
            self.copy_files_with_options()
    
    def copy_files_with_options(self):
        # Получаем активный слой
        layer = self.iface.activeLayer()
        if not layer:
            self.iface.messageBar().pushCritical("Error", self.tr("error_no_layer"))
            return
        
        # Диалог для выбора режима работы
        class ModeSelectionDialog(QDialog):
            def __init__(self, plugin, parent=None):
                super().__init__(parent)
                self.plugin = plugin
                self.setWindowTitle(self.plugin.tr("mode_selection"))
                self.setMinimumWidth(400)
                
                layout = QVBoxLayout()
                
                # Группа выбора режима
                mode_group = QGroupBox(self.plugin.tr("mode_group"))
                mode_layout = QVBoxLayout()
                
                self.mode_group_btns = QButtonGroup(self)
                self.mode_with_grouping = QRadioButton(self.plugin.tr("mode_with_grouping"))
                self.mode_without_grouping = QRadioButton(self.plugin.tr("mode_without_grouping"))
                
                self.mode_with_grouping.setChecked(True)
                
                self.mode_group_btns.addButton(self.mode_with_grouping, 1)
                self.mode_group_btns.addButton(self.mode_without_grouping, 2)
                
                mode_layout.addWidget(self.mode_with_grouping)
                mode_layout.addWidget(self.mode_without_grouping)
                mode_group.setLayout(mode_layout)
                
                layout.addWidget(mode_group)
                
                # Разделитель для нескольких файлов
                separator_group = QGroupBox(self.plugin.tr("multi_file_settings"))
                separator_layout = QVBoxLayout()
                
                separator_layout.addWidget(QLabel(self.plugin.tr("separator_label")))
                
                # Поле для ввода разделителя
                separator_widget = QHBoxLayout()
                separator_widget.addWidget(QLabel(self.plugin.tr("separator_prompt")))
                self.separator_input = QComboBox()
                self.separator_input.setEditable(True)
                self.separator_input.addItems([";", ",", "|", "\\t", "\\n"])
                self.separator_input.setCurrentText(";")
                separator_widget.addWidget(self.separator_input)
                separator_layout.addLayout(separator_widget)
                
                separator_group.setLayout(separator_layout)
                layout.addWidget(separator_group)
                
                # Кнопки OK/Cancel
                buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
                buttons.accepted.connect(self.accept)
                buttons.rejected.connect(self.reject)
                layout.addWidget(buttons)
                
                self.setLayout(layout)
            
            def get_mode(self):
                return self.mode_group_btns.checkedId()
            
            def get_separator(self):
                separator = self.separator_input.currentText()
                # Заменяем специальные символы
                if separator == "\\t":
                    return "\t"
                elif separator == "\\n":
                    return "\n"
                return separator if separator else ";"
        
        # Выбираем поле с путями к файлам
        fields = [field.name() for field in layer.fields()]
        
        file_field, ok = QInputDialog.getItem(
            None, self.tr("select_field"), self.tr("select_field_prompt"), fields, 0, False
        )
        
        if not ok:
            return
        
        # Диалог выбора режима
        mode_dialog = ModeSelectionDialog(self)
        if mode_dialog.exec_() != QDialog.Accepted:
            return
        
        mode = mode_dialog.get_mode()
        separator = mode_dialog.get_separator()
        
        if mode == 1:  # С группировкой
            self.copy_files_with_ordered_grouping(layer, file_field, separator)
        else:  # Без группировки
            self.copy_files_without_grouping(layer, file_field, separator)
    
    def extract_file_paths(self, file_value, separator):
        """Извлекает multiple файлов из значения атрибута"""
        if not file_value:
            return []
        
        file_paths = []
        # Пробуем разные методы разделения
        if separator in file_value:
            file_paths = [path.strip() for path in file_value.split(separator) if path.strip()]
        else:
            # Автоматическое определение разделителей
            possible_separators = [';', ',', '|', '\n', '\t']
            for sep in possible_separators:
                if sep in file_value:
                    file_paths = [path.strip() for path in file_value.split(sep) if path.strip()]
                    break
            
            # Если не нашли разделителей, используем весь текст как один путь
            if not file_paths:
                file_paths = [file_value.strip()]
        
        return file_paths
    
    def copy_files_without_grouping(self, layer, file_field, separator):
        """Копирование файлов без группировки"""
        # Выбираем папку для сохранения
        output_folder = QFileDialog.getExistingDirectory(
            None, self.tr("choose_folder"), ""
        )
        
        if not output_folder:
            return
        
        success_count = 0
        error_count = 0
        multi_file_count = 0
        
        # Создаем папку, если не существует
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Обрабатываем все объекты
        for feature in layer.getFeatures():
            file_value = feature[file_field]
            
            if not file_value:
                continue
            
            # Извлекаем все файлы из атрибута
            file_paths = self.extract_file_paths(str(file_value), separator)
            
            if len(file_paths) > 1:
                multi_file_count += 1
            
            # Копируем каждый файл
            for file_path in file_paths:
                if os.path.exists(file_path):
                    try:
                        file_name = os.path.basename(file_path)
                        destination = os.path.join(output_folder, file_name)
                        
                        # Обработка дубликатов имен файлов
                        counter = 1
                        base_name, extension = os.path.splitext(file_name)
                        while os.path.exists(destination):
                            new_file_name = f"{base_name}_{counter}{extension}"
                            destination = os.path.join(output_folder, new_file_name)
                            counter += 1
                        
                        shutil.copy2(file_path, destination)
                        success_count += 1
                        print(f"File copied: {file_name}")
                        
                    except Exception as e:
                        print(f"Error copying {file_path}: {str(e)}")
                        error_count += 1
                else:
                    print(f"File does not exist: {file_path}")
                    error_count += 1
        
        # Показываем результат
        self.iface.messageBar().pushInfo(
            self.tr("done"), 
            f"{self.tr('copied_files')} {success_count}\n"
            f"{self.tr('errors')} {error_count}\n"
            f"{self.tr('multi_file_objects')} {multi_file_count}"
        )
    
    def copy_files_with_ordered_grouping(self, layer, file_field, separator):
        """Копирование файлов с группировкой по атрибутам"""
        # Диалог для выбора порядка полей группировки
        class OrderedFieldSelectionDialog(QDialog):
            def __init__(self, plugin, fields, file_field, parent=None):
                super().__init__(parent)
                self.plugin = plugin
                self.setWindowTitle(self.plugin.tr("field_order_selection"))
                self.setMinimumWidth(500)
                self.setMinimumHeight(400)
                
                layout = QVBoxLayout()
                
                # Инструкция
                layout.addWidget(QLabel(self.plugin.tr("field_order_instruction")))
                
                # Основной layout
                main_layout = QHBoxLayout()
                
                # Левая панель - доступные поля
                left_layout = QVBoxLayout()
                left_layout.addWidget(QLabel(self.plugin.tr("available_fields")))
                self.available_list = QListWidget()
                for field in fields:
                    if field != file_field:
                        self.available_list.addItem(field)
                left_layout.addWidget(self.available_list)
                
                # Центральная панель - кнопки
                center_layout = QVBoxLayout()
                add_btn = QPushButton(self.plugin.tr("add_button"))
                add_btn.clicked.connect(self.add_field)
                remove_btn = QPushButton(self.plugin.tr("remove_button"))
                remove_btn.clicked.connect(self.remove_field)
                up_btn = QPushButton(self.plugin.tr("move_up"))
                up_btn.clicked.connect(self.move_up)
                down_btn = QPushButton(self.plugin.tr("move_down"))
                down_btn.clicked.connect(self.move_down)
                
                center_layout.addStretch()
                center_layout.addWidget(add_btn)
                center_layout.addWidget(remove_btn)
                center_layout.addWidget(up_btn)
                center_layout.addWidget(down_btn)
                center_layout.addStretch()
                
                # Правая панель - выбранные поля
                right_layout = QVBoxLayout()
                right_layout.addWidget(QLabel(self.plugin.tr("grouping_order")))
                self.selected_list = QListWidget()
                right_layout.addWidget(self.selected_list)
                
                main_layout.addLayout(left_layout)
                main_layout.addLayout(center_layout)
                main_layout.addLayout(right_layout)
                
                layout.addLayout(main_layout)
                
                # Кнопки OK/Cancel
                buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
                buttons.accepted.connect(self.accept)
                buttons.rejected.connect(self.reject)
                layout.addWidget(buttons)
                
                self.setLayout(layout)
            
            def add_field(self):
                current_item = self.available_list.currentItem()
                if current_item:
                    self.selected_list.addItem(current_item.text())
                    self.available_list.takeItem(self.available_list.row(current_item))
            
            def remove_field(self):
                current_item = self.selected_list.currentItem()
                if current_item:
                    self.available_list.addItem(current_item.text())
                    self.selected_list.takeItem(self.selected_list.row(current_item))
            
            def move_up(self):
                current_row = self.selected_list.currentRow()
                if current_row > 0:
                    item = self.selected_list.takeItem(current_row)
                    self.selected_list.insertItem(current_row - 1, item)
                    self.selected_list.setCurrentRow(current_row - 1)
            
            def move_down(self):
                current_row = self.selected_list.currentRow()
                if current_row < self.selected_list.count() - 1 and current_row >= 0:
                    item = self.selected_list.takeItem(current_row)
                    self.selected_list.insertItem(current_row + 1, item)
                    self.selected_list.setCurrentRow(current_row + 1)
            
            def get_ordered_fields(self):
                return [self.selected_list.item(i).text() for i in range(self.selected_list.count())]
        
        # Создаем диалог выбора порядка полей
        dialog = OrderedFieldSelectionDialog(self, [field.name() for field in layer.fields()], file_field)
        if dialog.exec_() != QDialog.Accepted:
            return
        
        ordered_fields = dialog.get_ordered_fields()
        if not ordered_fields:
            self.iface.messageBar().pushCritical("Error", self.tr("error_no_grouping_fields"))
            return
        
        # Выбираем папку для сохранения
        output_folder = QFileDialog.getExistingDirectory(
            None, self.tr("choose_root_folder"), ""
        )
        
        if not output_folder:
            return
        
        success_count = 0
        error_count = 0
        multi_file_count = 0
        
        # Функция для создания безопасного имени папки
        def create_safe_folder_name(name):
            if not name:
                return "unnamed"
            invalid_chars = '<>:"/\\|?*'
            for char in invalid_chars:
                name = name.replace(char, '_')
            name = name.strip('. ')
            return name[:30] if name else "unnamed"
        
        # Функция для создания иерархического пути
        def create_hierarchical_path(feature, fields):
            path_parts = []
            for field in fields:
                value = feature[field]
                if value:
                    safe_name = create_safe_folder_name(str(value))
                    path_parts.append(safe_name)
            return os.path.join(*path_parts) if path_parts else "unnamed_group"
        
        # Группируем объекты по иерархическому пути
        grouped_features = {}
        for feature in layer.getFeatures():
            hierarchical_path = create_hierarchical_path(feature, ordered_fields)
            if hierarchical_path not in grouped_features:
                grouped_features[hierarchical_path] = []
            grouped_features[hierarchical_path].append(feature)
        
        # Обрабатываем каждую группу
        for group_path, features in grouped_features.items():
            folder_path = os.path.join(output_folder, group_path)
            
            # Создаем папку со всей иерархией, если она еще не существует
            if not os.path.exists(folder_path):
                try:
                    os.makedirs(folder_path)
                    print(f"Folder created: {group_path}")
                except Exception as e:
                    print(f"Error creating folder {group_path}: {str(e)}")
                    error_count += len(features)
                    continue
            
            # Копируем все файлы из этой группы в соответствующую папку
            for feature in features:
                file_value = feature[file_field]
                
                if not file_value:
                    error_count += 1
                    continue
                
                # Извлекаем все файлы из атрибута
                file_paths = self.extract_file_paths(str(file_value), separator)
                
                if len(file_paths) > 1:
                    multi_file_count += 1
                
                for file_path in file_paths:
                    if os.path.exists(file_path):
                        try:
                            file_name = os.path.basename(file_path)
                            destination = os.path.join(folder_path, file_name)
                            
                            # Обработка дубликатов имен файлов
                            counter = 1
                            base_name, extension = os.path.splitext(file_name)
                            while os.path.exists(destination):
                                new_file_name = f"{base_name}_{counter}{extension}"
                                destination = os.path.join(folder_path, new_file_name)
                                counter += 1
                            
                            shutil.copy2(file_path, destination)
                            success_count += 1
                            print(f"File copied: {file_name} → {group_path}/")
                            
                        except Exception as e:
                            print(f"Error copying {file_path}: {str(e)}")
                            error_count += 1
                    else:
                        print(f"File does not exist: {file_path}")
                        error_count += 1
        
        # Показываем результат
        self.iface.messageBar().pushInfo(
            self.tr("done"), 
            f"{self.tr('hierarchical_folders')} {len(grouped_features)}\n"
            f"{self.tr('copied_files')} {success_count}\n"
            f"{self.tr('errors')} {error_count}\n"
            f"{self.tr('multi_file_objects')} {multi_file_count}"
        )