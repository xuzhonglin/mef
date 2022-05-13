-- 数据源
CREATE TABLE mef_source
(
    source_id                      TEXT NOT NULL,
    source_name                    TEXT NOT NULL,
    source_type                    TEXT NOT NULL,
    source_priority                INTEGER DEFAULT 999,
    source_home_page               TEXT,
    source_enable                  INTEGER DEFAULT 0,
    request_method                 TEXT,
    request_charset                TEXT    DEFAULT 'UTF-8',
    request_header                 TEXT,
    response_charset               TEXT    DEFAULT 'UTF-8',
    search_url                     TEXT,
    search_method                  TEXT,
    search_params                  TEXT,
    search_header                  TEXT,
    search_verify                  INTEGER DEFAULT 0,
    search_verify_url              TEXT,
    search_verify_submit_url       TEXT,
    search_result_list             TEXT,
    search_result_item_title       TEXT,
    search_result_item_url         TEXT,
    search_result_item_image       TEXT,
    search_result_item_status      TEXT,
    search_result_item_rating      TEXT,
    detail_page_title              TEXT,
    detail_page_image              TEXT,
    detail_page_description        TEXT,
    detail_page_line_list          TEXT,
    detail_page_line_name          TEXT,
    detail_page_episode_list       TEXT,
    detail_page_episode_item       TEXT,
    detail_page_episode_item_title TEXT,
    detail_page_episode_item_url   TEXT,
    play_page_title                TEXT,
    play_page_line_name            TEXT,
    play_page_line_config          TEXT,
    play_page_player_config_url    TEXT,
    play_page_player_url           TEXT,
    source_update_time             TEXT    DEFAULT (datetime('now', 'localtime'))
);

-- 代理配置
CREATE TABLE mef_proxy_config
(
    proxy_id           TEXT NOT NULL,
    proxy_name         TEXT NOT NULL,
    proxy_type         TEXT NOT NULL,
    proxy_host         TEXT NOT NULL,
    proxy_headers      TEXT,
    proxy_replacements TEXT,
    proxy_enable       INTEGER DEFAULT 0,
    proxy_update_time  TEXT    DEFAULT (datetime('now', 'localtime'))
);

-- 数据字典
CREATE TABLE mef_dictionary
(
    dict_id          TEXT NOT NULL,
    dict_name        TEXT NOT NULL,
    dict_type        TEXT NOT NULL,
    dict_content     TEXT,
    dict_enable      INTEGER DEFAULT 0,
    dict_update_time TEXT    DEFAULT (datetime('now', 'localtime'))
);


CREATE TABLE mef_result_cache
(

);