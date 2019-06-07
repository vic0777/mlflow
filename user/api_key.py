#encoding:utf-8
'''
Created on 2019/6/4

@author: vic
'''

class ApiKey:
    @staticmethod
    def generate(username):
        #仅演示用，需要换成真正的实现
        return hash(username)
    
