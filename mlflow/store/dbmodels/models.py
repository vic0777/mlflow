#coding:utf-8

import time
from sqlalchemy.orm import relationship, backref
from sqlalchemy import (
    Column, String, Float, ForeignKey, Integer, CheckConstraint,
    BigInteger, PrimaryKeyConstraint)
from sqlalchemy.ext.declarative import declarative_base
from mlflow.entities import (
    Experiment, RunTag, Metric, Param, RunData, RunInfo,
    SourceType, RunStatus, Run, ViewType, User, Project, Workspace, ProjectInfo, WorkspaceInfo, ExperimentInfo)
from mlflow.entities.lifecycle_stage import LifecycleStage
from Demos.win32ts_logoff_disconnected import username

Base = declarative_base()


SourceTypes = [
    SourceType.to_string(SourceType.NOTEBOOK),
    SourceType.to_string(SourceType.JOB),
    SourceType.to_string(SourceType.LOCAL),
    SourceType.to_string(SourceType.UNKNOWN),
    SourceType.to_string(SourceType.PROJECT)
]

RunStatusTypes = [
    RunStatus.to_string(RunStatus.SCHEDULED),
    RunStatus.to_string(RunStatus.FAILED),
    RunStatus.to_string(RunStatus.FINISHED),
    RunStatus.to_string(RunStatus.RUNNING)
]

"""
AgileAI新增的表
"""
class SqlOnlineUser(Base):
    """
    DB model for users of agileai.com. These are recorded in ``online_users`` table
    """
    __tablename__ = 'online_users'
    
    user_id = Column(Integer, autoincrement=True)
    """
    user_id: primary key of table ``online_users``
    """
    username = Column(String(256), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    api_key = Column(String(50), unique=True, nullable=False)
    register_time = Column(BigInteger, default=int(time.time()))
    
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='online_user_pk'),
    )

    def __repr__(self):
        return '<SqlOnlineUser ({}, {})>'.format(self.user_id, self.username)
    
    def _to_mlflow_entity(self):
        return User(user_id=str(self.user_id), username=self.username, email=self.email, 
                    api_key=self.api_key, register_time=self.register_time)
    
class SqlWorkspace(Base):
    """
    DB model for workspace of agileai.com. These are recorded in ``workspace`` table       
    """
    __tablename__ = 'workspaces'
    
    workspace_id = Column(Integer, autoincrement=True)
    """
    workspace_id: primary key of table ``workspaces``
    """ 
    name = Column(String(256), nullable=False)
    """
          同一个用户的workspace不能有重名的，不同用户不限制。要在程序代码里进行约束。
    """
    user_id = Column(Integer, ForeignKey('online_users.user_id'))
    """
    user_id: 外键， online_user表的user_id列
    """
    description = Column(String(1000))
    create_time = Column(BigInteger, default=int(time.time()))
    
    __table_args__ = (
        PrimaryKeyConstraint('workspace_id', name='workspace_pk'),
    )
    
    def __repr__(self):
        return '<SqlWorkspace ({}, {})>'.format(self.workspace_id, self.name)
        
    def _to_mlflow_entity(self):
        """
        :return: :py:class:`mlflow.entities.Workspace`
        """
        project_info_list = []
        project_info_list.extend([project.get_project_info() for project in self.projects])
        workspace_info = WorkspaceInfo(self.workspace_id, self.user_id, self.name, self.description, 
                                       len(self.projects), self.create_time)
        
        return Workspace(workspace_info, project_info_list)
    
    def _get_workspace_info(self):
        """
        create a WorkspaceInfo object and return it
        :return: :py:class:`mlflow.entities.WorkspaceInfo`
        """
        return WorkspaceInfo(self.workspace_id, self.user_id, self.name, self.description, 
                           len(self.projects), self.create_time)        
        
class SqlProject(Base):
    """
    DB model for project of agileai.com. These are recorded in ``project`` table
        注意：与mlflow的project不同，这个是网站上的project ！！！。 
    """

    __tablename__ = 'projects'
    
    project_id = Column(Integer, autoincrement=True)
    workspace_id = Column(Integer, ForeignKey('workspaces.workspace_id'))
    """
    workspace_id:外键， workspaces表的workspace_id列
    """
    name = Column(String(256), nullable=False)
    """
         同一个workspace的project不能有重名的，不同workspace的不限制。要在程序代码里进行约束。
    """
    description = Column(String(1000))
    create_time = Column(BigInteger, default=int(time.time()))
    
    workspace = relationship('SqlWorkspace', backref=backref('projects', cascade='all'))
    
    __table_args__ = (
        PrimaryKeyConstraint('project_id', name='project_pk'),
    )
    
    def __repr__(self):
        return '<SqlProject ({}, {})>'.format(self.project_id, self.name)
    
    def _get_project_info(self):
        """
        create a ProjectInfo object and return it
        :return: :py:class:`mlflow.entities.ProjectInfo`
        """
        return ProjectInfo(self.project_id, self.workspace_id, self.name, self.description, 
                           len(self.experiments), self.create_time)
    
    def _to_mlflow_entity(self):
        """
        :return: :py:class: `mlflow.entities.Project`
        """
        experiment_info_list = []
        experiment_info_list.extend([experiment.get_experiment_info() for experiment in self.experiments])
        project_info = ProjectInfo(self.project_id, self.workspace_id, self.name, self.description, 
                                       len(self.experiments), self.create_time)
        
        return Project(project_info, experiment_info_list)
        
        
"""
==================================================================================================
mlflow原有的表
"""    
class SqlExperiment(Base):
    """
    DB model for :py:class:`mlflow.entities.Experiment`. These are recorded in ``experiment`` table.
    """
    __tablename__ = 'experiments'

    experiment_id = Column(Integer, autoincrement=True)
    """
    Experiment ID: `Integer`. *Primary Key* for ``experiment`` table.
    """
    project_id = Column(Integer, ForeignKey('project.project_id'))
    name = Column(String(256), unique=True, nullable=False)
    """
    Experiment name: `String` (limit 256 characters). Defined as *Unique* and *Non null* in
                     table schema.
    """
    artifact_location = Column(String(256), nullable=True)
    """
    Default artifact location for this experiment: `String` (limit 256 characters). Defined as
                                                    *Non null* in table schema.
    """
    lifecycle_stage = Column(String(32), default=LifecycleStage.ACTIVE)
    """
    Lifecycle Stage of experiment: `String` (limit 32 characters).
                                    Can be either ``active`` (default) or ``deleted``.
    """
    description = Column(String(1000))
    create_time = Column(BigInteger, default=int(time.time()))

    project = relationship('SqlProject', backref=backref('experiments', cascade='all'))
    
    __table_args__ = (
        CheckConstraint(
            lifecycle_stage.in_(LifecycleStage.view_type_to_stages(ViewType.ALL)),
            name='experiments_lifecycle_stage'),
        PrimaryKeyConstraint('experiment_id', name='experiment_pk')
    )

    def __repr__(self):
        return '<SqlExperiment ({}, {})>'.format(self.experiment_id, self.name)

    def to_mlflow_entity(self):
        """
        Convert DB model to corresponding MLflow entity.

        :return: :py:class:`mlflow.entities.Experiment`.
        """
        return Experiment(
            experiment_id=str(self.experiment_id),
            project_id=str(self.project_id),
            name=self.name,
            artifact_location=self.artifact_location,
            lifecycle_stage=self.lifecycle_stage,
            desc=self.description,
            create_time=self.create_time)
    
    def get_experiment_info(self):
        """
        create a ExperimentInfo object and return it
        :return: :py:class:`mlflow.entities.ExperimentInfo`
        """
        return ExperimentInfo(self.experiment_id, self.project_id, self.name, self.description, 
                           len(self.runs), self.create_time)


class SqlRun(Base):
    """
    DB model for :py:class:`mlflow.entities.Run`. These are recorded in ``runs`` table.
    """
    __tablename__ = 'runs'

    run_uuid = Column(String(32), nullable=False)
    """
    Run UUID: `String` (limit 32 characters). *Primary Key* for ``runs`` table.
    """
    name = Column(String(250))
    """
    Run name: `String` (limit 250 characters).
    """
    source_type = Column(String(20), default=SourceType.to_string(SourceType.LOCAL))
    """
    Source Type: `String` (limit 20 characters). Can be one of ``NOTEBOOK``, ``JOB``, ``PROJECT``,
                 ``LOCAL`` (default), or ``UNKNOWN``.
    """
    source_name = Column(String(500))
    """
    Name of source recording the run: `String` (limit 500 characters).
    """
    entry_point_name = Column(String(50))
    """
    Entry-point name that launched the run run: `String` (limit 50 characters).
    """
    user_id = Column(String(256), nullable=True, default=None)
    """
    User ID: `String` (limit 256 characters). Defaults to ``null``.
    """
    
    status = Column(String(20), default=RunStatus.to_string(RunStatus.SCHEDULED))
    """
    Run Status: `String` (limit 20 characters). Can be one of ``RUNNING``, ``SCHEDULED`` (default),
                ``FINISHED``, ``FAILED``.
    """
    start_time = Column(BigInteger, default=int(time.time()))
    """
    Run start time: `BigInteger`. Defaults to current system time.
    """
    end_time = Column(BigInteger, nullable=True, default=None)
    """
    Run end time: `BigInteger`.
    """
    source_version = Column(String(50))
    """
    Source version: `String` (limit 50 characters).
    """
    lifecycle_stage = Column(String(20), default=LifecycleStage.ACTIVE)
    """
    Lifecycle Stage of run: `String` (limit 32 characters).
                            Can be either ``active`` (default) or ``deleted``.
    """
    artifact_uri = Column(String(200), default=None)
    """
    Default artifact location for this run: `String` (limit 200 characters).
    """
    experiment_id = Column(Integer, ForeignKey('experiments.experiment_id'))
    """
    Experiment ID to which this run belongs to: *Foreign Key* into ``experiment`` table.
    """
    experiment = relationship('SqlExperiment', backref=backref('runs', cascade='all'))
    """
    SQLAlchemy relationship (many:one) with :py:class:`mlflow.store.dbmodels.models.SqlExperiment`.
    """

    __table_args__ = (
        CheckConstraint(source_type.in_(SourceTypes), name='source_type'),
        CheckConstraint(status.in_(RunStatusTypes), name='status'),
        CheckConstraint(lifecycle_stage.in_(LifecycleStage.view_type_to_stages(ViewType.ALL)),
                        name='runs_lifecycle_stage'),
        PrimaryKeyConstraint('run_uuid', name='run_pk')
    )

    def to_mlflow_entity(self):
        """
        Convert DB model to corresponding MLflow entity.

        :return: :py:class:`mlflow.entities.Run`.
        """
        run_info = RunInfo(
            run_uuid=self.run_uuid,
            run_id=self.run_uuid,
            experiment_id=str(self.experiment_id),
            user_id=self.user_id,
            status=self.status,
            start_time=self.start_time,
            end_time=self.end_time,
            lifecycle_stage=self.lifecycle_stage,
            artifact_uri=self.artifact_uri)

        # only get latest recorded metrics per key
        all_metrics = [m.to_mlflow_entity() for m in self.metrics]
        metrics = {}
        for m in all_metrics:
            existing_metric = metrics.get(m.key)
            if (existing_metric is None)\
                or ((m.step, m.timestamp, m.value) >=
                    (existing_metric.step, existing_metric.timestamp,
                        existing_metric.value)):
                metrics[m.key] = m

        run_data = RunData(
            metrics=list(metrics.values()),
            params=[p.to_mlflow_entity() for p in self.params],
            tags=[t.to_mlflow_entity() for t in self.tags])

        return Run(run_info=run_info, run_data=run_data)


class SqlTag(Base):
    """
    DB model for :py:class:`mlflow.entities.RunTag`. These are recorded in ``tags`` table.
    """
    __tablename__ = 'tags'

    key = Column(String(250))
    """
    Tag key: `String` (limit 250 characters). *Primary Key* for ``tags`` table.
    """
    value = Column(String(250), nullable=True)
    """
    Value associated with tag: `String` (limit 250 characters). Could be *null*.
    """
    run_uuid = Column(String(32), ForeignKey('runs.run_uuid'))
    """
    Run UUID to which this tag belongs to: *Foreign Key* into ``runs`` table.
    """
    run = relationship('SqlRun', backref=backref('tags', cascade='all'))
    """
    SQLAlchemy relationship (many:one) with :py:class:`mlflow.store.dbmodels.models.SqlRun`.
    """

    __table_args__ = (
        PrimaryKeyConstraint('key', 'run_uuid', name='tag_pk'),
    )

    def __repr__(self):
        return '<SqlRunTag({}, {})>'.format(self.key, self.value)

    def to_mlflow_entity(self):
        """
        Convert DB model to corresponding MLflow entity.

        :return: :py:class:`mlflow.entities.RunTag`.
        """
        return RunTag(
            key=self.key,
            value=self.value)


class SqlMetric(Base):
    __tablename__ = 'metrics'

    key = Column(String(250))
    """
    Metric key: `String` (limit 250 characters). Part of *Primary Key* for ``metrics`` table.
    """
    value = Column(Float, nullable=False)
    """
    Metric value: `Float`. Defined as *Non-null* in schema.
    """
    timestamp = Column(BigInteger, default=lambda: int(time.time()))
    """
    Timestamp recorded for this metric entry: `BigInteger`. Part of *Primary Key* for
                                               ``metrics`` table.
    """
    step = Column(BigInteger, default=0, nullable=False)
    """
    Step recorded for this metric entry: `BigInteger`.
    """
    run_uuid = Column(String(32), ForeignKey('runs.run_uuid'))
    """
    Run UUID to which this metric belongs to: Part of *Primary Key* for ``metrics`` table.
                                              *Foreign Key* into ``runs`` table.
    """
    run = relationship('SqlRun', backref=backref('metrics', cascade='all'))
    """
    SQLAlchemy relationship (many:one) with :py:class:`mlflow.store.dbmodels.models.SqlRun`.
    """

    __table_args__ = (
        PrimaryKeyConstraint('key', 'timestamp', 'step', 'run_uuid', 'value', name='metric_pk'),
    )

    def __repr__(self):
        return '<SqlMetric({}, {}, {}, {})>'.format(self.key, self.value, self.timestamp, self.step)

    def to_mlflow_entity(self):
        """
        Convert DB model to corresponding MLflow entity.

        :return: :py:class:`mlflow.entities.Metric`.
        """
        return Metric(
            key=self.key,
            value=self.value,
            timestamp=self.timestamp,
            step=self.step)


class SqlParam(Base):
    __tablename__ = 'params'

    key = Column(String(250))
    """
    Param key: `String` (limit 250 characters). Part of *Primary Key* for ``params`` table.
    """
    value = Column(String(250), nullable=False)
    """
    Param value: `String` (limit 250 characters). Defined as *Non-null* in schema.
    """
    run_uuid = Column(String(32), ForeignKey('runs.run_uuid'))
    """
    Run UUID to which this metric belongs to: Part of *Primary Key* for ``params`` table.
                                              *Foreign Key* into ``runs`` table.
    """
    run = relationship('SqlRun', backref=backref('params', cascade='all'))
    """
    SQLAlchemy relationship (many:one) with :py:class:`mlflow.store.dbmodels.models.SqlRun`.
    """

    __table_args__ = (
        PrimaryKeyConstraint('key', 'run_uuid', name='param_pk'),
    )

    def __repr__(self):
        return '<SqlParam({}, {})>'.format(self.key, self.value)

    def to_mlflow_entity(self):
        """
        Convert DB model to corresponding MLflow entity.

        :return: :py:class:`mlflow.entities.Param`.
        """
        return Param(
            key=self.key,
            value=self.value)
