-- *********************************************
-- * SQL MySQL generation                      
-- *--------------------------------------------
-- * DB-MAIN version: 10.0.1              
-- * Generator date: Jan 10 2017              
-- * Generation date: Wed Apr 19 19:19:16 2017 
-- * LUN file: D:\working\denning\Dennnig IT Office.lun 
-- * Schema: Relational Model/1-1 
-- ********************************************* 


-- Database Section
-- ________________ 

create database Relational Model;
use Relational Model;


-- Tables Section
-- _____________ 

create table Address (
     id bigint not null AUTO_INCREMENT,
     street varchar(255),
     info_id bigint,
     constraint IDaddress primary key (id));

create table Checklist (
     id bigint not null AUTO_INCREMENT,
     code varchar(255),
     description text,
     constraint IDChecklist_ID primary key (id));

create table Contact (
     id bigint not null AUTO_INCREMENT,
     id_type bigint,
     name varchar(255),
     title varchar(255),
     citizenship varchar(255),
     type varchar(255),
     Info_id bigint,
     constraint IDContact primary key (id));

create table Contact_Info (
     id bigint not null AUTO_INCREMENT,
     postcode varchar(255),
     town varchar(255),
     state varchar(255),
     country varchar(255),
     fax varchar(255),
     website varchar(255),
     contact_person varchar(255),
     mail_preference varchar(255),
     constraint IDContact_Info_ID primary key (id));

create table Attribute (
     id bigint not null AUTO_INCREMENT,
     value varchar(255),
     type varchar(255),
     constraint IDAttribute primary key (id));

create table Group (
     id bigint not null AUTO_INCREMENT,
     name varchar(255),
     constraint IDGroup_ID primary key (id));

create table Matter (
     id varchar(255),
     checklist_id bigint,
     file_number varchar(255),
     open_date date,
     status varchar(255),
     related varchar(255),
     pocket_location varchar(255),
     physical_location varchar(255),
     box_location varchar(255),
     close_date date,
     turnaround int,
     billing_code varchar(255),
     remarks text,
     additional_info text,
     code_id bigint,
     constraint IDMatter_ID primary key (id),
     constraint FKhas_checklist_ID unique (checklist_id));

create table Matter_Code (
     id bigint not null AUTO_INCREMENT,
     related_id bigint,
     code varchar(255),
     matter text,
     category varchar(255),
     departement varchar(255),
     turnaround int,
     billing_code varchar(255),
     favourites char,
     additional_info text,
     checklist_id bigint,
     constraint IDMatter_Code_ID primary key (id),
     constraint FKEdit_form_ID unique (related_id));

create table Normal (
     id bigint not null AUTO_INCREMENT,
     contact_id char(1),
     email varchar(255),
     old_ic varchar(255),
     addtional_info text,
     constraint IDNormal primary key (id),
     constraint FKis_normal_ID unique (contact_id));

create table Phone (
     id bigint not null AUTO_INCREMENT,
     phone_number varchar(255),
     type varchar(255),
     info_id bigint,
     constraint IDPhone primary key (id));

create table privilege (
     id bigint not null AUTO_INCREMENT,
     title varchar(255),
     parent bigint,
     constraint IDprivilege_ID primary key (id));

create table Property (
     id bigint not null AUTO_INCREMENT,
     type varchar(255),
     individual char,
     title_type varchar(255),
     title_no varchar(255),
     lot_type varchar(255),
     lot_no varchar(255),
     daerah varchar(255),
     negeri varchar(255),
     area varchar(255),
     tenure varchar(255),
     lease_expiry_date date,
     title_registeration_date date,
     interest varchar(255),
     restriction_against varchar(255),
     approving_authority varchar(255),
     other_restriction varchar(255),
     category_land_use varchar(255),
     express_condition varchar(255),
     building_type varchar(255),
     building_age int,
     postal_address varchar(255),
     assessment_rate decimal(10,2),
     annual_quit_rent decimal(10,2),
     previous_title varchar(255),
     additional_info text,
     constraint IDProperty primary key (id));

create table grant (
     group_id bigint,
     privilega_id bigint,
     constraint IDgrant primary key (privilega_id, group_id));

create table Matter_Contact (
     matter_id varchar(255),
     contact_id char(1),
     type varchar(255),
     constraint IDhas_contact primary key (matter_id, contact_id));

create table Staff (
     id bigint not null AUTO_INCREMENT,
     contact_id char(1),
     login_id varchar(100),
     password varchar(255),
     nickname bigint,
     marital char,
     spouse_name varchar(255),
     number_children int,
     qualification varchar(255),
     department varchar(255),
     position_type varchar(255),
     monthly_salary int,
     prev_adjustment_date date,
     annual_leave int,
     date_commenced date,
     date_ceased date,
     tenure_employed varchar(255),
     status varchar(100),
     tax_file_no int,
     socso_no int,
     epf_no int,
     remarks text,
     group_id bigint,
     constraint IDStaff primary key (id),
     constraint FKis_staff_ID unique (contact_id));

create table Task (
     id bigint not null AUTO_INCREMENT,
     code varchar(255),
     description text,
     status varchar(255),
     category varchar(255),
     start_date date,
     after varchar(255),
     est_time date,
     due_date date,
     done_date date,
     remarks text,
     checklist_id bigint,
     constraint IDTask primary key (id));

create table Template (
     id varchar(100) not null AUTO_INCREMENT,
     name varchar(255),
     path varchar(255),
     date date,
     language varchar(255),
     type varchar(255),
     matter_id varchar(255),
     task_id bigint,
     constraint IDTemplate primary key (id));


-- Constraints Section
-- ___________________ 

alter table Address add constraint FKhas_address
     foreign key (info_id)
     references Contact_Info (id);

-- Not implemented
-- alter table Checklist add constraint IDChecklist_CHK
--     check(exists(select * from Matter
--                  where Matter.checklist_id = id)); 

alter table Contact add constraint FKinfo
     foreign key (Info_id)
     references Contact_Info (id);

-- Not implemented
-- alter table Contact_Info add constraint IDContact_Info_CHK
--     check(exists(select * from Phone
--                  where Phone.info_id = id)); 

-- Not implemented
-- alter table Contact_Info add constraint IDContact_Info_CHK
--     check(exists(select * from Address
--                  where Address.info_id = id)); 

-- Not implemented
-- alter table Contact_Info add constraint IDContact_Info_CHK
--     check(exists(select * from Contact
--                  where Contact.Info_id = id)); 

-- Not implemented
-- alter table Group add constraint IDGroup_CHK
--     check(exists(select * from grant
--                  where grant.group_id = id)); 

-- Not implemented
-- alter table Matter add constraint IDMatter_CHK
--     check(exists(select * from Matter_Contact
--                  where Matter_Contact.matter_id = id)); 

alter table Matter add constraint FKhas_matter_code
     foreign key (code_id)
     references Matter_Code (id);

alter table Matter add constraint FKhas_checklist_FK
     foreign key (checklist_id)
     references Checklist (id);

-- Not implemented
-- alter table Matter_Code add constraint IDMatter_Code_CHK
--     check(exists(select * from Matter_Code
--                  where Matter_Code.related_id = id)); 

alter table Matter_Code add constraint FKEdit_form_FK
     foreign key (related_id)
     references Matter_Code (id);

alter table Matter_Code add constraint FKMC_CL
     foreign key (checklist_id)
     references Checklist (id);

alter table Normal add constraint FKis_normal_FK
     foreign key (contact_id)
     references Contact (id);

alter table Phone add constraint FKhas_phone
     foreign key (info_id)
     references Contact_Info (id);

-- Not implemented
-- alter table privilege add constraint IDprivilege_CHK
--     check(exists(select * from grant
--                  where grant.privilega_id = id)); 

alter table grant add constraint FKgra_pri
     foreign key (privilega_id)
     references privilege (id);

alter table grant add constraint FKgra_Gro
     foreign key (group_id)
     references Group (id);

alter table Matter_Contact add constraint FKhas_Con
     foreign key (contact_id)
     references Contact (id);

alter table Matter_Contact add constraint FKhas_Mat
     foreign key (matter_id)
     references Matter (id);

alter table Staff add constraint FKbelong_to
     foreign key (group_id)
     references Group (id);

alter table Staff add constraint FKis_staff_FK
     foreign key (contact_id)
     references Contact (id);

alter table Task add constraint FKhas_task
     foreign key (checklist_id)
     references Checklist (id);

alter table Template add constraint FKmatter_template
     foreign key (matter_id)
     references Matter (id);

alter table Template add constraint FKhas_template
     foreign key (task_id)
     references Task (id);


-- Index Section
-- _____________ 

