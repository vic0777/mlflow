#encoding:utf-8
'''
Created on 2019/6/3

@author: vic
'''

from mlflow.entities._mlflow_object import _MLflowObject
from mlflow.protos.service_pb2 import WorkspaceInfo as ProtoWorkspaceInfo

class WorkspaceInfo(_MLflowObject):
    #TODO: 把这个类与Workspace合并，基本重复，无需单独写一个类。
    
    def __init__(self, workspace_id, user_id, name, desc, num_of_project, create_time):
        self._workspace_id = workspace_id
        self._user_id = user_id        
        self._name = name
        self._desc = desc
        self._num_of_project = num_of_project
        self._create_time = create_time
        
    @property
    def user_id(self):
        """
        :return: user id(string)
        """
        return self._user_id
    
    @property
    def workspace_id(self):
        """
        :return: workspace id(string)
        """
        return self._workspace_id
        
    @property
    def name(self):
        return self._name
    
    @property
    def desc(self):
        return self._desc
    
    @property
    def num_of_project(self):
        return self._num_of_project
    
    @property
    def create_time(self):
        return self._create_time
    
    @classmethod
    def from_proto(cls, proto):
        return cls(proto.workspace_id, proto.user_id, proto.name, proto.desc, 
                   proto.num_of_project, proto.create_time)
    
    def to_proto(self):
        proto = ProtoWorkspaceInfo()
        proto.workspace_id = self.workspace_id
        proto.user_id = self.user_id        
        proto.name = self.name
        proto.desc = self.desc
        proto.num_of_project = self.num_of_project
        proto.create_time = self.create_time