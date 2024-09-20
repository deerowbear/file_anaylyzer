```How to Run
py .\file_anaylyzer.py --src 'D:\work\pic\working' --output 'D:\work\pic\output' 

```Query
SELECT length(create_date) as length from photos where length < 10;
SELECT * from photos where file_name like '%20730|%' 
SELECT * from photos where is_duplicate = 'True' and file_path not like '%_archive%';
SELECT * FROM copied_photos where file_name like '%72C.jpg%' and is_duplicate = 'False';
SELECT count(*) from photos where is_duplicate = 'True';
SELECT count(*) FROM photos where is_duplicate = 'False'; 
SELECT * FROM photos where file_name like '%IMG_20171208_103807_1.jpg%' and is_duplicate = 'False';
sqlite3 -header -csv ~/Desktop/projects/python-learning/photos.db  "select * from photos;" > photos.csv
CREATE TABLE copied_photos AS SELECT * FROM photos WHERE 0
drop table copied_photos;
select count(*) from photos where file_name  not in (select file_name from copied_photos);
select count(*) from photos where file_name in (select file_name from copied_photos);
SELECT count(*) FROM photos where is_copy = 'False';
SELECT count(*) FROM photos where is_written = 'False' and is_copy = 'False';
select parsename(file_name,1)  from photos;
SELECT   substr(file_name, 1, instr(file_name, ' ') - 1) AS file_name FROM photos
SELECT substr(file_name, length(file_name)-3, length(file_name)-3) as extenstion from photos;   
select length(file_name)  from photos;  
SELECT DISTINCT SUBSTRING_INDEX(file_name, ' ', 1) FROM photos;
SELECT substr(file_name, length(file_name)-3, length(file_name)-3) from photos where is_written='False' GROUP BY substr(file_name, length(file_name)-3, length(file_name)-3) ;
select * from photos where is_written = 'False' and file_name like '%.MP4%'
SELECT file_name FROM photos where is_written = 'False' and is_copy = 'False' and file_name not like '%.pi2%';