import sys

from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as omui


class RetimingToolUi(QtWidgets.QDialog):

    WINDOW_TITLE = "Retiming Tool"

    ABSOLUTE_BUTTON_WIDTH = 50
    RELATIVE_BUTTON_WIDTH = 64
    
    RETIMING_PROPERTY_NAME = "retiming_data"

    @classmethod
    def maya_main_window(cls):
        """
        Return the Maya main window widget as a Python object
        """
        main_window_ptr = omui.MQtUtil.mainWindow()
        if sys.version_info.major >= 3:
            return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
        else:
            return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

    def __init__(self):
        super(RetimingToolUi, self).__init__(self.maya_main_window())

        self.setWindowTitle(self.WINDOW_TITLE)
        if cmds.about(ntOS=True):
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        elif cmds.about(macOS=True):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.absolute_btns = []
        for i in range(1,7):
            btn = QtWidgets.QPushButton("{0}f".format(i))
            btn.setFixedWidth(self.ABSOLUTE_BUTTON_WIDTH)
            btn.setProperty(self.RETIMING_PROPERTY_NAME, [i,False])
            self.absolute_btns.append(btn)
        
        self.reletive_btns = []
        for i in [-2,-1,1,2]:
            btn = QtWidgets.QPushButton("{0}f".format(i))
            btn.setFixedWidth(self.RELATIVE_BUTTON_WIDTH)
            btn.setProperty(self.RETIMING_PROPERTY_NAME, [i,True])
            self.reletive_btns.append(btn)
        
        self.move_to_next_cb = QtWidgets.QCheckBox("move to next frame")

    def create_layouts(self):
        absolute_btns_layout = QtWidgets.QHBoxLayout()
        absolute_btns_layout.setSpacing(2)
        for btn in self.absolute_btns:
            absolute_btns_layout.addWidget(btn)
        
        reletive_btns_layout = QtWidgets.QHBoxLayout()
        reletive_btns_layout.setSpacing(2)
        for btn in self.reletive_btns:
            reletive_btns_layout.addWidget(btn)
            if reletive_btns_layout.count() == 2:
                reletive_btns_layout.addStretch()
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.setSpacing(2)
        main_layout.addLayout(absolute_btns_layout)
        main_layout.addLayout(reletive_btns_layout)
        main_layout.addWidget(self.move_to_next_cb)
        
                

    def create_connections(self):
        for btn in self.absolute_btns:
            btn.clicked.connect(self.retime)
        
        for btn in self.reletive_btns:
            btn.clicked.connect(self.retime)
    
    def retime(self):
        btn = self.sender()
        if btn:
            retime_data = btn.property(self.RETIMING_PROPERTY_NAME)
            move_to_next = self.move_to_next_cb.isChecked()
            #call retime_keys function in utile class
            print(retime_data[0], retime_data[1], move_to_next)


if __name__ == "__main__":

    try:
        retiming_ui.close() # pylint: disable=E0601
        retiming_ui.deleteLater()
    except:
        pass

    retiming_ui = RetimingToolUi()
    retiming_ui.show()