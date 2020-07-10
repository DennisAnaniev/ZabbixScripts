set pagesize 0
set trimspool on
set headsep off
select targetsystem || '_' || operation || '_' || stage || ',' || evnt_cnt
from IIBNRT.ESBEVENT_COUNTER
where sample_start_time= (select max(sample_start_time) from IIBNRT.ESBEVENT_COUNTER);
exit
  