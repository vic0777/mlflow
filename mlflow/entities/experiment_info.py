#encoding:utf-8
'''
Created on 2019/6/3

@author: vic
'''
from mlflow.entities._mlflow_object import _MLflowObject
from mlflow.protos.service_pb2 import ExperimentInfo as ProtoExperimentInfo

class ExperimentInfo(_MLflowObject):
    def __init__(self, experiment_id, project_id, name, desc, num_of_run, create_time):
        self._experiment_id = experiment_id
        self._project_id = project_id
        self._name = name
        self._desc = desc
        self._num_of_run = num_of_run
        self._create_time = create_time
    
    @property
    def experiment_id(self):
        return self._experiment_id
    
    @property
    def project_id(self):
        return self._project_id
        
    @property
    def name(self):
        return self._name
    
    @property
    def desc(self):
        return self._desc
    
    @property
    def num_of_run(self):
        return self._num_of_run
    
    @property
    def create_time(self):
        return self._create_time
    
    @classmethod
    def from_proto(cls, proto):
        return cls(proto.experiment_id, proto.project_id, proto.name, proto.desc, 
                   proto.num_of_run, proto.create_time)
    
    def to_proto(self):
        proto = ProtoExperimentInfo()
        proto.experiment_id = self.experiment_id
        proto.project_id = self.project_id
        proto.name = self.name
        proto.desc = self.desc
        proto.num_of_run = self.num_of_run
        proto.create_time = self.create_time
        
        return proto
    