from PySide6.QtWidgets import QGroupBox, QGridLayout, QPushButton, QWidget
from pyside6helpers import group, Hourglass, icons
from pyside6helpers.error_reporting import error_reported
from pyside6helpers.table_view import resize_columns_to_content_with_padding


from tdcdesktopapp.core.entity.gui.entity_table import EntityTable
from tdcdesktopapp.components.multiplayer.client import MultiplayerClient
from tdcdesktopapp.components.project.api import ProjectsApi


class ProjectsWidget(QGroupBox):

    def __init__(self, parent=None):
        QGroupBox.__init__(self, parent)

        self._projects = list()
        self._api = ProjectsApi()

        self.setTitle("Projects")

        self._entity_table = EntityTable(self._api)
        self._entity_table.dataReloadRequested.connect(self.reload)

        self._button_add = QPushButton("Add Project")
        self._button_add.setIcon(icons.plus())
        self._button_add.clicked.connect(self._add_project)

        self._button_remove = QPushButton("Remove Project")
        self._button_remove.setIcon(icons.cancel())
        self._button_remove.clicked.connect(self._entity_table.remove_entity)

        self._button_reload = QPushButton("Reload")
        self._button_reload.setIcon(icons.refresh())
        self._button_reload.setMinimumWidth(170)
        self._button_reload.clicked.connect(self.reload)

        layout = QGridLayout(self)
        layout.addWidget(self._entity_table.view, 0, 0, 3, 1)
        layout.addWidget(group.make_group("Operations", [self._button_add, self._button_remove]), 0, 1)
        layout.addWidget(QWidget(), 1, 1)
        layout.addWidget(self._button_reload, 2, 1)
        layout.setRowStretch(1, 100)

        MultiplayerClient().signals.projectsReloadRequested.connect(self.reload)

    @error_reported("Load projects")
    def reload(self):
        with Hourglass():
            projects = self._api.get()
            self._entity_table.set_entities(projects)
            resize_columns_to_content_with_padding(self._entity_table.view, 10)

    @error_reported("New project")
    def _add_project(self):
        self._api.new()
        self.reload()
