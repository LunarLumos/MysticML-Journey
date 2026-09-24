# Module 2 – MySQL User Management
> Week 2 · Data Analysis with MySQL   |   ⬅ Previous: [Module 1 – Introduction](../Module_1_Introduction_to_MySQL)  ·  Next ➡: [Module 3 – Database](../Module_3_MySQL_Database)

## 🎯 Learning Objectives
- Create accounts and understand the `'user'@'host'` identity.
- Grant, inspect and revoke privileges following the **principle of least privilege**.
- List users, change passwords, lock accounts, and drop users.

## ✅ Syllabus Checklist
- [x] Create User | Grant Privileges to User
- [x] Show All Users | Drop User | Change User Password

## 📖 Concepts

### Accounts
An account is **user + host**: `'aadil'@'localhost'` and `'aadil'@'%'` are two *different* accounts.
`localhost` = only from this machine, `%` = from any host, `'192.168.1.%'` = from a subnet.
Accounts are stored in the system table `mysql.user`.

### Syntax cheat-sheet
| Task | Statement |
|------|-----------|
| Create user | `CREATE USER IF NOT EXISTS 'ana'@'localhost' IDENTIFIED BY 'S3cret!';` |
| Grant on one DB | `GRANT SELECT, INSERT ON shop.* TO 'ana'@'localhost';` |
| Grant on one table / column | `GRANT UPDATE (title) ON shop.reports TO 'ana'@'localhost';` |
| Show privileges | `SHOW GRANTS FOR 'ana'@'localhost';` · `SHOW GRANTS;` (yourself) |
| Show all users | `SELECT user, host FROM mysql.user;` |
| Who am I | `SELECT USER(), CURRENT_USER();` |
| Change password | `ALTER USER 'ana'@'localhost' IDENTIFIED BY 'N3w!';` · own: `ALTER USER USER() IDENTIFIED BY '…';` |
| Lock / unlock | `ALTER USER 'ana'@'localhost' ACCOUNT LOCK;` / `ACCOUNT UNLOCK` |
| Rename | `RENAME USER 'ana'@'localhost' TO 'anna'@'localhost';` |
| Revoke | `REVOKE INSERT ON shop.* FROM 'ana'@'localhost';` |
| Roles (8.0+) | `CREATE ROLE 'readonly'; GRANT SELECT ON shop.* TO 'readonly'; GRANT 'readonly' TO 'ana'@'localhost';` |
| Drop user | `DROP USER IF EXISTS 'ana'@'localhost';` |

### Privilege levels
| Level | Written as | Example |
|-------|-----------|---------|
| Global | `*.*` | admin accounts only |
| Database | `db.*` | an app's own schema |
| Table | `db.table` | reporting user |
| Column | `UPDATE (col) ON db.table` | edit one field only |

Common privileges: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `ALTER`, `DROP`, `INDEX`, `EXECUTE`, `ALL PRIVILEGES`. `WITH GRANT OPTION` lets the user pass privileges on – give it sparingly.

Expected `SHOW GRANTS FOR 'mystic_dev'@'%';` result (illustrative) after the grants in `02_user_management_complete.sql`:

| Grants for mystic_dev@% |
|---|
| GRANT USAGE ON \*.\* TO \`mystic_dev\`@\`%\` |
| GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER ON \`mysticml_user_mgmt\`.\* TO \`mystic_dev\`@\`%\` |
| GRANT \`mystic_readonly\`@\`%\` TO \`mystic_dev\`@\`%\` |

(`USAGE` means "can log in, no other privileges".)

## 📂 Files in this Module
| File | What it demonstrates |
|------|----------------------|
| `mysql_user_management.sql` | *Learner's original:* list users, create `Aadil`, grant/revoke on `my_database`, show grants, drop user |
| `02_user_management_complete.sql` | Full lifecycle: list users, create users (with password policy), database/column grants, `SHOW GRANTS`, roles, `ALTER USER` password / lock, `RENAME USER`, `REVOKE`, `DROP USER` – cleans up after itself (DB `mysticml_user_mgmt`) |

## ▶️ How to Run
> ⚠️ These scripts change **server-wide accounts**. Run them only on your **own local practice server**, connected as an admin. The companion script was reviewed but intentionally **not executed** while building this repo.
```bash
cd Week_2_Data_Analysis_with_MySQL/Module_2_MySQL_User_Management
mysql -u root -p < 02_user_management_complete.sql
# test the new account in another terminal while it exists:
mysql -u mystic_analyst -p mysticml_user_mgmt
```

## 🧠 Key Takeaways
- Identity = `'user'@'host'`; the host part matters.
- Grant the **minimum** privileges a user needs, on the narrowest scope.
- Use roles to manage privileges for many users at once.
- Never share the root account with applications.

## 📝 Practice Exercises
1. Create `'report_bot'@'localhost'` that can only `SELECT` from `mysticml_sales` (Module 7 dataset). Try an `INSERT` as that user – what error do you get?
2. Create a role `sales_editor` with `SELECT, INSERT, UPDATE` on `mysticml_sales.*` and grant it to two users.
3. Force a password expiry with `ALTER USER … PASSWORD EXPIRE;` and log in – what happens?
4. Write the statements to remove everything you created in 1–3.
