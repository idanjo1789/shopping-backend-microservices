USE store_db;
CREATE TABLE IF NOT EXISTS chat_sessions (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NOT NULL,
  session_key VARCHAR(64) NOT NULL,
  prompts_used INT NOT NULL DEFAULT 0,
  max_prompts INT NOT NULL DEFAULT 5,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  PRIMARY KEY (id),
  UNIQUE KEY uq_chat_session_key (session_key),
  KEY idx_chat_user_id (user_id),
  KEY idx_chat_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;