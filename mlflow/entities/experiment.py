from mlflow.entities._mlflow_object import _MLflowObject
from mlflow.protos.service_pb2 import Experiment as ProtoExperiment
from mlflow.entities.run_info import RunInfo

class Experiment(_MLflowObject):
    """
    Experiment object.
    """
    DEFAULT_EXPERIMENT_NAME = "Default"

    def __init__(self, experiment_id, name, artifact_location, lifecycle_stage, desc, num_of_run, run_info):
        """
        :param experiment_id:
        :param name:
        :param artifact_location:
        :param lifecycle_stage:
        :param desc:
        :param num_of_run: number of run belong to this experiment
        :param run_info: List of :py:class:`mlflow.entities.RunInfo`
        """
        super(Experiment, self).__init__()
        self._experiment_id = experiment_id
        self._name = name
        self._artifact_location = artifact_location
        self._lifecycle_stage = lifecycle_stage
        
        #added by AgileAI
        self._desc = desc
        self._num_of_run = num_of_run
        self._run_info = run_info

    @property
    def experiment_id(self):
        """String ID of the experiment."""
        return self._experiment_id

    @property
    def name(self):
        """String name of the experiment."""
        return self._name

    def _set_name(self, new_name):
        self._name = new_name

    @property
    def artifact_location(self):
        """String corresponding to the root artifact URI for the experiment."""
        return self._artifact_location

    @property
    def lifecycle_stage(self):
        """Lifecycle stage of the experiment. Can either be 'active' or 'deleted'."""
        return self._lifecycle_stage
    
    @property
    def desc(self):
        return self._desc
    
    @property
    def num_of_run(self):
        return self._num_of_run
    
    @property
    def run_info(self):
        return self._run_info
    
        
    @classmethod
    def from_proto(cls, proto):
        info_list = []
        info_list.append(RunInfo.from_proto(element) for element in proto.run_info)
        
        return cls(proto.experiment_id, proto.name, proto.artifact_location, proto.lifecycle_stage, 
                   proto.desc, proto.num_of_run, info_list)

    def to_proto(self):
        proto = ProtoExperiment()
        proto.experiment_id = self.experiment_id
        proto.name = self.name
        proto.artifact_location = self.artifact_location
        proto.lifecycle_stage = self.lifecycle_stage
        proto.desc = self.desc
        proto.num_of_run = self.num_of_run
        proto.run_info.extend([element.to_proto() for element in self.run_info])
        
        return proto
