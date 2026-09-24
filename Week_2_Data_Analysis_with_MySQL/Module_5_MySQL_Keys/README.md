# Module 5 – MySQL Keys
> Week 2 · Data Analysis with MySQL   |   ⬅ Previous: [Module 4 – Tables & Views](../Module_4_Tables_Views)  ·  Next ➡: [Module 6 – Queries & Constraints](../Module_6_MySQL_Queries_Constraints)

## 🎯 Learning Objectives
- Identify rows with **primary** and **composite** keys.
- Prevent duplicates with **unique** keys.
- Link tables and protect referential integrity with **foreign** keys and `ON DELETE` / `ON UPDATE` actions.

## ✅ Syllabus Checklist
- [x] Unique Key
- [x] Primary Key
- [x] Composite Key
- [x] Foreign Key

## 📖 Concepts

| Key | Rule | NULL allowed? | How many per table | Syntax |
|-----|------|---------------|--------------------|--------|
| **Primary key** | uniquely identifies each row | ❌ | exactly one | `id INT PRIMARY KEY` or `PRIMARY KEY (id)` |
| **Unique key** | no duplicate values | ✅ (many NULLs) | many | `email VARCHAR(100) UNIQUE` or `CONSTRAINT uq UNIQUE (brand, model)` |
| **Composite key** | a primary (or unique) key over 2+ columns – the *combination* must be unique | ❌ | – | `PRIMARY KEY (order_id, sku)` |
| **Foreign key** | value must exist in the parent table's key | ✅ (means "no parent") | many | `FOREIGN KEY (customer_id) REFERENCES customers(customer_id)` |

Every key automatically creates an **index**, which also speeds up lookups and joins.

### Foreign-key actions
| Action | When the parent row is deleted / its key updated |
|--------|---------------------------------------------------|
| `RESTRICT` / `NO ACTION` (default) | refuse (error 1451) |
| `CASCADE` | delete / update the child rows too |
| `SET NULL` | set the child's FK column to NULL |

```
customers (PK customer_id) 1───∞ orders (PK order_id, FK customer_id) 1───∞ order_items (PK order_id+sku) ∞───1 products (PK sku)
```

### Errors keys prevent (real messages from `02_keys_complete.sql`)
| Attempt | Error |
|---------|-------|
| duplicate primary key | `ERROR 1062: Duplicate entry 'LP-14' for key 'products.PRIMARY'` |
| duplicate unique email | `ERROR 1062: Duplicate entry 'aadil@example.com' for key 'customers.uq_customers_email'` |
| duplicate composite key | `ERROR 1062: Duplicate entry '1-LP-14' for key 'order_items.PRIMARY'` |
| order for missing customer | `ERROR 1452: Cannot add or update a child row: a foreign key constraint fails` |

### Managing keys
| Task | Statement |
|------|-----------|
| Add PK later | `ALTER TABLE products ADD PRIMARY KEY (sku);` |
| Add unique | `ALTER TABLE products ADD CONSTRAINT uq_brand_model UNIQUE (brand, model);` |
| Drop unique | `ALTER TABLE customers DROP INDEX uq_customers_phone;` |
| Drop FK | `ALTER TABLE order_items DROP FOREIGN KEY fk_items_product;` |
| Drop PK | `ALTER TABLE t DROP PRIMARY KEY;` |
| Inspect | `SHOW KEYS FROM t;` · `information_schema.table_constraints` / `key_column_usage` |

## 📂 Files in this Module
| File | What it demonstrates |
|------|----------------------|
| `mysql_keys.sql` | *Learner's original:* students / courses / enrollments with primary, unique, composite and foreign keys (DB `school_management`) |
| `02_keys_complete.sql` | Named constraints, PK added via `ALTER`, multi-column unique key, composite PK, FKs with `CASCADE`/`RESTRICT`, commented-out statements that trigger each error, cascade delete demo, inspecting & dropping keys (DB `mysticml_keys`) |

## ▶️ How to Run
```bash
cd Week_2_Data_Analysis_with_MySQL/Module_5_MySQL_Keys
mysql -u root -p -t < 02_keys_complete.sql
# then open `mysql -u root -p mysticml_keys` and paste the commented "violation" statements one by one
```

## 🧠 Key Takeaways
- Primary key = identity (unique + not null, one per table); unique key = "no duplicates" rule.
- Composite keys model "this combination may appear only once" (e.g. a student in a course).
- Foreign keys keep related tables consistent; pick `CASCADE`, `SET NULL` or `RESTRICT` deliberately.

## 📝 Practice Exercises
1. Design `authors`, `books`, `book_authors` (many-to-many) with the right PKs and FKs.
2. Change `fk_orders_customer` to `ON DELETE RESTRICT` (drop and re-add it) and try deleting a customer.
3. Add a unique key so a customer cannot place two orders on the same date.
4. Query `information_schema.key_column_usage` to draw the relationships of `mysticml_keys` on paper.
