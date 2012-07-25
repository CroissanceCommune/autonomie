update egw_accounts set account_primary_group=3 where account_primary_group!= -10 and account_primary_group != -14;
update egw_accounts set account_primary_group=1 where account_primary_group=-10;
update egw_accounts set account_primary_group=2 where account_primary_group=-14;

