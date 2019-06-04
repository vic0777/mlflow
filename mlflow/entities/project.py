#encoding:utf-8
'''
Created on 2019/6/3

@author: vic
'''
from mlflow.entities._mlflow_object import _MLflowObject
from mlflow.protos.service_pb2 import Project as ProtoProject
from mlflow.entities.experiment_info import ExperimentInfo

class Project(_MLflowObject):
    def __init__(self, project_info, experiment_info):
        """
        :param project_info: :py:class:`mlflow.entries.ProjectInfo`
        :param experiment_info: List of :py:class:`mlflow.entries.ExperimentInfo`
        """
        self._project_info = project_info
        self._experiment_info = experiment_info
        
    @property
    def project_info(self):
        """
        The project metadata, such as name, desc, the number of experiments belong to this project
        :rtype: :py:class:`mlflow.entities.ProjectInfo`
        """
        return self._project_info
    
    @property
    def experiment_info(self):
        """
        The metadata of experiments belong to this project, such as name, desc, the number of runs 
        belong to this experiment.
        :rtype: :List of :py:class`mlflow.entries.ExperimentInfo`
        """
        return self._experiment_info
    
    @classmethod
    def from_proto(cls, proto):
        project_info = proto.info
        experiment_info = []
        for info in proto.experiment_info:
            experiment_info.append(ExperimentInfo.from_proto(info))
        
        return cls(project_info, experiment_info)
    
    def to_proto(self):
        proto = ProtoProject()
        proto.info = self.project_info
        proto.experiment_info.extend([e.to_proto() for e in self.experiment_info])
        
        return proto
        