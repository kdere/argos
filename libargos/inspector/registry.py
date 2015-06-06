# -*- coding: utf-8 -*-
# This file is part of Argos.
# 
# Argos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Argos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Argos. If not, see <http://www.gnu.org/licenses/>.

""" Defines a global Inspector registry to register plugins.
"""

import logging

from libargos.qt.registry import ClassRegItem, ClassRegistry, GRP_REGISTRY

logger = logging.getLogger(__name__)

GRP_REGISTRY_INSPECTORS = GRP_REGISTRY + '/inspectors'

class InspectorRegItem(ClassRegItem): # TODO: rename to InspectorRegItem? InspectorPlugin?
    """ Class to keep track of a registered Inspector.
        Has a create() method that functions as an Inspector factory.
    """
    
    def __init__(self, identifier, fullClassName, pythonPath=''):
        """ Constructor. See the ClassRegItem class doc string for the parameter help.
        """
        super(InspectorRegItem, self).__init__(identifier, fullClassName, pythonPath=pythonPath)

        
    @property
    def axesNames(self):
        """ The axes names of the inspector.
        """
        return [] if self.cls is None else self.cls.axesNames() 

    @property
    def nDims(self):
        """ The number of axes of this inspector.
        """
        return len(self.axesNames)
    
    
    def create(self, collector, tryImport=True):
        """ Creates an inspector of the registered and passes the collector to the constructor.
            Tries to import the class if tryImport is True.
            Raises ImportError if the class could not be imported.
        """
        cls = self.getClass(tryImport=tryImport)
        if not self.successfullyImported:
            raise ImportError("Class not successfully imported: {}".format(self.exception))
        return cls(collector)


class InspectorRegistry(ClassRegistry):
    """ Class that maintains the collection of registered inspector classes.
        See the base class documentation for more info.
    """
    def __init__(self, settingsGroupName=GRP_REGISTRY_INSPECTORS):
        """ Constructor
        """
        super(InspectorRegistry, self).__init__(settingsGroupName=settingsGroupName)
        self._itemClass = InspectorRegItem
            
            
    def registerInspector(self, identifier, fullClassName, pythonPath=''):
        """ Registers an Inspector class.
        """
        regInspector = InspectorRegItem(identifier, fullClassName, pythonPath=pythonPath)
        self.registerItem(regInspector)

    
    def getDefaultItems(self):
        """ Returns a list with the default plugins in the inspector registry.
        """
        return [    
            InspectorRegItem('Empty Inspector', 'libargos.inspector.empty.EmptyInspector'), 
            InspectorRegItem('Qt/Table', 'libargos.inspector.table.TableInspector'), 
            InspectorRegItem('PyQtGraph/1D Line Plot', 
                             'libargos.inspector.pgplugins.lineplot1d.PgLinePlot1d')]
            
