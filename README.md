# planit-backend
AX Academy 4기 3팀 중간프로젝트 Planit  백엔드 Repository

# DB 수정사항
-- 세부 일정 (place_name, place_address 정규화 필요)
CREATE TABLE schedule (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    trip_day_id BIGINT,                     
    place_id BIGINT,        -- place_name, place_address 삭제 + places 테이블과 FK로 연결
    schedule_content TEXT,                  
    start_time TIME,                        
    end_time TIME,                          
    schedule_datetime DATETIME NOT NULL,    
    FOREIGN KEY (trip_day_id) REFERENCES trip_day(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE SET NULL     -- places 테이블과 FK로 연결
);

-- 준비물 체크리스트
CREATE TABLE checklist_item (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    trip_id BIGINT,     -- trip_day에서 trip으로 연결 테이블 변경
    item_name VARCHAR(255) NOT NULL,
    is_checked BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (trip_id) REFERENCES trip(id) on delete cascade
);