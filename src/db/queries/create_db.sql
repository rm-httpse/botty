CREATE SCHEMA IF NOT EXISTS machine;

CREATE TABLE IF NOT EXISTS machine.reg_user (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    hostname TEXT NOT NULL,
    os_name TEXT NOT NULL,
    os_version TEXT NOT NULL,
    registered_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (username, hostname)
);

CREATE SCHEMA "app";

CREATE TABLE app."alias" (
  "id" uuid PRIMARY KEY NOT NULL,
  "action_id" uuid,
  "description" varchar,
  "created_at" date DEFAULT now()
);

CREATE TABLE app."action" (
  "id" uuid PRIMARY KEY NOT NULL,
  "platform_id" uuid NOT NULL,
  "category_id" uuid,
  "description" varchar,
  "created_at" date DEFAULT now()
);

CREATE TABLE os."platform" (
  "id" uuid PRIMARY KEY NOT NULL,
  "name" varchar NOT NULL UNIQUE,
  "metadata" jsonb DEFAULT '{}'::jsonb,
  "created_at" timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE app."category" (
  "id" uuid PRIMARY KEY NOT NULL,
  "description" varchar,
  "metadata" jsonb,
  "created_at" date DEFAULT now()
);

CREATE TABLE app."instruction" (
  "id" uuid PRIMARY KEY NOT NULL,
  "element_id" uuid,
  "description" varchar,
  "type" varchar,
  "input_text" varchar,
  "created_at" date DEFAULT now()
);

CREATE TABLE app."action_instruction" (
  "action_id" uuid NOT NULL,
  "instruction_id" uuid NOT NULL,
  "position" integer NOT NULL
);

CREATE TABLE app."element" (
  "id" uuid PRIMARY KEY NOT NULL,
  "name" varchar,
  "image_path" varchar,
  "metadata" jsonb,
  "created_at" date DEFAULT now()
);

CREATE TABLE app."state" (
  "id" uuid PRIMARY KEY NOT NULL,
  "current_action_id" uuid,
  "current_instruction_id" uuid,
  "status" varchar
);

CREATE TABLE app."state_change" (
  "id" uuid PRIMARY KEY NOT NULL,
  "state_id" uuid,
  "from_status" varchar,
  "to_status" varchar,
  "timestamp" timestamptz DEFAULT now(),
  "metadata" jsonb
);

CREATE TABLE app."error_log" (
  "id" uuid PRIMARY KEY NOT NULL,
  "instruction_id" uuid,
  "type" varchar,
  "description" varchar,
  "resolved" bool,
  "created_at" timestamptz DEFAULT now()
);

CREATE TABLE app."edge_case" (
  "id" uuid PRIMARY KEY NOT NULL,
  "description" varchar,
  "related_instruction_id" uuid,
  "solution" varchar
);

CREATE UNIQUE INDEX "pk_action_instruction" ON app."action_instruction" ("action_id", "instruction_id");

ALTER TABLE app."alias" ADD FOREIGN KEY ("action_id") REFERENCES app."action" ("id");

ALTER TABLE app."action" ADD FOREIGN KEY ("category_id") REFERENCES app."category" ("id");

ALTER TABLE app."instruction" ADD FOREIGN KEY ("element_id") REFERENCES app."element" ("id");

ALTER TABLE app."action_instruction" ADD FOREIGN KEY ("action_id") REFERENCES app."action" ("id");

ALTER TABLE app."action_instruction" ADD FOREIGN KEY ("instruction_id") REFERENCES app."instruction" ("id");

ALTER TABLE app."state" ADD FOREIGN KEY ("current_action_id") REFERENCES app."action" ("id");

ALTER TABLE app."state" ADD FOREIGN KEY ("current_instruction_id") REFERENCES app."instruction" ("id");

ALTER TABLE app."state_change" ADD FOREIGN KEY ("state_id") REFERENCES app."state" ("id");

ALTER TABLE app."error_log" ADD FOREIGN KEY ("instruction_id") REFERENCES app."instruction" ("id");

ALTER TABLE app."edge_case" ADD FOREIGN KEY ("related_instruction_id") REFERENCES app."instruction" ("id");

ALTER TABLE app."action" ADD COLUMN "platform_id" uuid NOT NULL, ADD FOREIGN KEY ("platform_id") REFERENCES app."platform" ("id");