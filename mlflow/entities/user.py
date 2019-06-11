#coding:utf-8

'''
Created on 2019/6/3
@author: vic
'''

from mlflow.entities._mlflow_object import _MLflowObject
from mlflow.protos.service_pb2 import User as ProtoUser

class User(_MLflowObject):
    def __init__(self, user_id, username, email, api_key, register_time):
        """_register_time: in number of milliseconds since the UNIX epoch."""
        self._user_id = user_id
        self._username = username
        self._email = email
        self._api_key = api_key
        self._register_time = register_time
        
    @property
    def user_id(self):
        """
        :return: user id(string)
        """
        return self._user_id
    
    @property
    def username(self):
        return self._username
    
    @property
    def email(self):
        return self._email
    
    @property
    def api_key(self):
        return self._api_key
    
    @property
    def register_time(self):
        return self._register_time
    
    @classmethod
    def from_proto(cls, proto):
        return cls(proto.user_id, proto.username, proto.email, proto.api_key, proto.register_time)
    
    def to_proto(self):
        proto = ProtoUser()
        proto.user_id = self.user_id
        proto.username = self.username
        proto.email = self.email
        proto.api_key = self.api_key
        proto.register_time = self.register_time
        



