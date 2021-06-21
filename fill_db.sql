use mydb;

call fill_db();
call update_cgs(1, 'updated_cgs', 'new_location');
call update_highway(1, 'update_highway', 1);
call update_campus(1, 'updated_capmus', 1);
call update_address(1, 'updated2', 2, 2, 2, 3);
call delete_address_by_id(2); 