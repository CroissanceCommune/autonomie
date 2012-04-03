INSERT into egw_accounts  (`account_lid`, `account_pwd`, `account_firstname` ,`account_lastname`, `account_email`) VALUES ('user1_login', '24c9e15e52afc47c225b757e7bee1f9d', 'user1_firstname', 'user1_lastname', 'user1@test.fr');
INSERT into coop_company (`name`, `object`, `phone`, `creationDate`, `updateDate`, `IDGroup`, `IDEGWUser`) VALUES ('company1', 'Company of user1', '0457858585', '1286804741', '1286804741', '0', '0');
INSERT into coop_company_employee (`IDCompany`, `IDEmployee`) VALUES ('1', '1');
INSERT into coop_customer (`code`, `name`, `creationDate`, `updateDate`, `IDCompany`) VALUES ('C001', 'Client1', '1286804741', '1286804741', '1');
INSERT into coop_project (`name`, `customerCode`, `code`, `definition`, `creationDate`, `updateDate`, `status`, `IDCompany`) VALUES ('Projet de test', 'C001', 'P001', 'Projet de test', '1286804741', '1286804741', '', '1');
