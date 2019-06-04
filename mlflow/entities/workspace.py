'''
Created on 2019/6/3

@author: vic
'''

from mlflow.entities._mlflow_object import _MLflowObject
from mlflow.protos.service_pb2 import Workspace as ProtoWorkspace
from mlflow.entities.project_info import ProjectInfo
from docs.source.conf import project

class Workspace(_MLflowObject):
    def __init__(self, info, project_info):
        """
        :param info: :py:class:`mlflow.entities.WorkspaceInfo`
        :param project_info: List of :py:class:`mlflow.entities.ProjectInfo`
        """
        self._info = info
        self._project_info = project_info
    
    @property
    def info(self):
        return self._info
    
    @property
    def project_info(self):
        return self._project_info
    
    @classmethod
    def from_proto(cls, proto):
        info = proto.info
        project_info = []
        project_info.append(ProjectInfo.from_proto(element) for element in proto.project_info)
        
        return cls(info, project_info)
    
    def to_proto(self):
        proto = ProtoWorkspace
        proto.info = self.info
        proto.project_info.extend([element.to_proto() for element in self.project_info])
        
        return proto