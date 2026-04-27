CREATE TABLE rag_document (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NULL,
    title VARCHAR(200) NOT NULL,
    content MEDIUMTEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'general',
    tags VARCHAR(255) DEFAULT '',
    source VARCHAR(50) DEFAULT 'manual',
    status VARCHAR(20) DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KEY idx_user_status (user_id, status),
    KEY idx_category_status (category, status),
    KEY idx_updated_at (updated_at)
);
