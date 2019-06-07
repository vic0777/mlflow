'''
Created on 2019/6/3

@author: vic
'''

from mlflow.entities._mlflow_object import _MLflowObject
from mlflow.protos.service_pb2 import WorkspaceInfoList as ProtoWorkspaceInfoList
from mlflow.entities.workspace_info import WorkspaceInfo


class WorkspaceInfoList(_MLflowObject):
    """
    List of metadata of workspaces belong to a user, such as workspace name, desc, and number of project 
    belong to the workspace
    """
    def __init__(self, ws_info):
        """
        :param ws_info: List of :py:class:`mlflow.entities.WorkspaceInfo`
        """
        self._ws_info = ws_info
        
    @property
    def workspace_info(self):
        return self._ws_info
    
    @classmethod
    def from_proto(cls, proto):
        info_list = []
        info_list.append(WorkspaceInfo.from_proto(proto_info) for proto_info in proto.ws_info)
        
        return cls(list)
    
    def to_proto(self):
        proto = ProtoWorkspaceInfoList()
        proto.ws_info.extend([info.to_proto() for info in self.workspace_info])
        
        return proto