-- Disable all accounts with no enterprise
update egw_accounts as egwa left outer join coop_company_employee as cce on egwa.account_id=cce.IDEmployee set account_status='I' where cce.IDEmployee is null;
-- Enable all accounts part from the 1 and 2 group (admins)
update egw_accounts set account_status='A' where account_primary_group in (1,2);
