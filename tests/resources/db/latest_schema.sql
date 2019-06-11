
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
)


CREATE TABLE experiments (
	experiment_id INTEGER NOT NULL, 
	name VARCHAR(256) NOT NULL, 
	artifact_location VARCHAR(256), 
	lifecycle_stage VARCHAR(32), 
	project_id INTEGER NOT NULL,
	description VARCHAR(256),
	create_time BIGINT,
	CONSTRAINT experiment_pk PRIMARY KEY (experiment_id),
	FOREIGN KEY(project_id) REFERENCES projects (project_id), 
	UNIQUE (name), 
	CONSTRAINT experiments_lifecycle_stage CHECK (lifecycle_stage IN ('active', 'deleted'))
)


CREATE TABLE runs (
	run_uuid VARCHAR(32) NOT NULL, 
	name VARCHAR(250), 
	source_type VARCHAR(20), 
	source_name VARCHAR(500), 
	entry_point_name VARCHAR(50), 
	user_id VARCHAR(256), 
	status VARCHAR(20), 
	start_time BIGINT, 
	end_time BIGINT, 
	source_version VARCHAR(50), 
	lifecycle_stage VARCHAR(20), 
	artifact_uri VARCHAR(200), 
	experiment_id INTEGER, 
	CONSTRAINT run_pk PRIMARY KEY (run_uuid), 
	FOREIGN KEY(experiment_id) REFERENCES experiments (experiment_id), 
	CONSTRAINT status CHECK (status IN ('SCHEDULED', 'FAILED', 'FINISHED', 'RUNNING')), 
	CONSTRAINT source_type CHECK (source_type IN ('NOTEBOOK', 'JOB', 'LOCAL', 'UNKNOWN', 'PROJECT')), 
	CONSTRAINT runs_lifecycle_stage CHECK (lifecycle_stage IN ('active', 'deleted'))
)


CREATE TABLE metrics (
	key VARCHAR(250) NOT NULL, 
	value FLOAT NOT NULL, 
	timestamp BIGINT NOT NULL, 
	run_uuid VARCHAR(32) NOT NULL, 
	step BIGINT DEFAULT '0' NOT NULL, 
	CONSTRAINT metric_pk PRIMARY KEY (key, value, timestamp, run_uuid, step), 
	FOREIGN KEY(run_uuid) REFERENCES runs (run_uuid)
)


CREATE TABLE params (
	key VARCHAR(250) NOT NULL, 
	value VARCHAR(250) NOT NULL, 
	run_uuid VARCHAR(32) NOT NULL, 
	CONSTRAINT param_pk PRIMARY KEY (key, run_uuid), 
	FOREIGN KEY(run_uuid) REFERENCES runs (run_uuid)
)


CREATE TABLE tags (
	key VARCHAR(250) NOT NULL, 
	value VARCHAR(250), 
	run_uuid VARCHAR(32) NOT NULL, 
	CONSTRAINT tag_pk PRIMARY KEY (key, run_uuid), 
	FOREIGN KEY(run_uuid) REFERENCES runs (run_uuid)
)


/*--------------------------------------- Added by AgileAI-------------------------------------------------------------*/
CREATE TABLE online_users (
	user_id INTEGER NOT NULL, 
	user_name VARCHAR(256) NOT NULL, 
	password VARCHAR(256) NOT NULL,
	email VARCHAR(256) NOT NULL,
	api_key VARCHAR(256) NOT NULL,
	register_time BIGINT,
	CONSTRAINT user_pk PRIMARY KEY (user_id), 
	UNIQUE (name), 
	UNIQUE (email)	
)

CREATE TABLE workspaces (
	workspace_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL,
	name VARCHAR(256) NOT NULL, 
	description VARCHAR(256),	
	create_time BIGINT,
	CONSTRAINT workspace_pk PRIMARY KEY (workspace_id), 
	FOREIGN KEY(user_id) REFERENCES online_users (user_id)	
)

CREATE TABLE projects (
	project_id INTEGER NOT NULL, 
	workspace_id INTEGER NOT NULL,
	name VARCHAR(256) NOT NULL, 
	description VARCHAR(256),	
	create_time BIGINT,
	CONSTRAINT project_pk PRIMARY KEY (project_id), 
	FOREIGN KEY(workspace_id) REFERENCES workspaces (workspace_id)	
)























