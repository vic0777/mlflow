'''
Created on 2019/6/3

@author: vic
'''

from mlflow.entities._mlflow_object import _MLflowObject
from mlflow.protos.service_pb2 import WorkspaceInfo as ProtoWorkspaceInfo

class WorkspaceInfo(_MLflowObject):
    def __init__(self, id, name, desc, num_of_project):
        self._id = id
        self._name = name
        self._desc = desc
        self._num_of_project = num_of_project
    
    @property
    def id(self):
        return self._id
        
    @property
    def name(self):
        return self._name
    
    @property
    def desc(self):
        return self._desc
    
    @property
    def num_of_project(self):
        return self._num_of_project
    
    @classmethod
    def from_proto(cls, proto):
        return cls(proto.id, proto.name, proto.desc, proto.num_of_project)
    
    def to_proto(self):
        proto = ProtoWorkspaceInfo()
        proto.id = self.id
        proto.name = self.name
        proto.desc = self.desc
        proto.num_of_project = self.num_of_project
        