#encoding:utf-8
'''
Created on 2019/6/3

@author: vic
'''

from mlflow.entities._mlflow_object import _MLflowObject
from mlflow.protos.service_pb2 import ProjectInfo as ProtoProjectInfo

class ProjectInfo(_MLflowObject):
    #TODO: 把这个类与Project合并，基本重复，无需单独写一个类。
    
    def __init__(self, project_id, workspace_id, name, desc, num_of_experiment, create_time):
        self._project_id = project_id
        self._workspace_id = workspace_id
        self._name = name
        self._desc = desc
        self._num_of_experiment = num_of_experiment
        self._create_time = create_time
    
    @property
    def workspace_id(self):
        """
        :return: workspace id(string)
        """
        return self._workspace_id
    
    @property
    def project_id(self):
        """
        :return: project id(string)
        """
        return self._project_id
    
    @property
    def name(self):
        return self._name
    
    @property
    def desc(self):
        return self._desc
    
    @property
    def num_of_experiment(self):
        return self._num_of_experiment
    
    @property
    def create_time(self):
        return self._create_time
    
    @classmethod
    def from_proto(cls, proto):
        return cls(proto.project_id, proto.workspace_id, proto.name, proto.desc, 
                   proto.num_of_experiment, proto.create_time)
    
    def to_proto(self):
        proto = ProtoProjectInfo()
        proto.project_id = self.project_id
        proto.workspace_id = self.workspace_id
        proto.name = self.name
        proto.desc = self.desc
        proto.num_of_experiment = self.num_of_experiment
        proto.create_time = self.create_time
        
        return proto