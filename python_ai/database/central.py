class CentralDB:
    # Existing methods ...

    def upsert_records(self, table_name, records):
        if not records:
            return
        cursor = self.conn.cursor()
        columns = records[0].keys()
        col_str = ",".join(columns)
        placeholder = ",".join(["%s"]*len(columns))
        update_str = ",".join([f"{c}=VALUES({c})" for c in columns])

        sql = f"INSERT INTO {table_name} ({col_str}) VALUES ({placeholder}) ON DUPLICATE KEY UPDATE {update_str}"
        for r in records:
            cursor.execute(sql, tuple(r[c] for c in columns))
        self.conn.commit()
        cursor.close()
