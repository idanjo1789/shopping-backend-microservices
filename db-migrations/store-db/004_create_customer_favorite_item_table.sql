USE store_db;
CREATE TABLE IF NOT EXISTS customer_favorite_item (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NOT NULL,
  item_id BIGINT UNSIGNED NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  PRIMARY KEY (id),
  UNIQUE KEY uq_fav_user_item (user_id, item_id),
  KEY idx_fav_user_id (user_id),
  KEY idx_fav_item_id (item_id),

  CONSTRAINT fk_fav_item
    FOREIGN KEY (item_id) REFERENCES items(id)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;