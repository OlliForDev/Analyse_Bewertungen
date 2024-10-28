DELIMITER $$

CREATE PROCEDURE create_dwh()
BEGIN
	#DECLARE CONTINUE HANDLER FOR SQLWARNING BEGIN END;
    
	#############################
	# build initale stage schema
	#############################
	drop schema if exists stage;
	Create schema if not exists stage;
	
	drop table if exists stage.provider;
	create table if not exists stage.provider(
		pvr_id int primary key auto_increment,
		pvr_name varchar(125),
		pvr_foundation_year varchar(4),
		pvr_number_of_employees varchar(5),
		pvr_number_of_customer varchar(12),
		pvr_revenue varchar(14),
		pvr_post_code varchar(5)
	);

	drop table if exists stage.ratings;
	create table if not exists stage.ratings(
		rts_id int primary key auto_increment,
		rts_title varchar(125),
		rts_scoring_price varchar(3),
		rts_scoring_provider_change varchar(3),
		rts_scoring_service varchar(3),
		rts_date_of_order varchar(20),
		rts_date_of_change varchar(20)    
	);
    
END $$

DELIMITER ;