class LocalDB:
    # Existing methods ...

    def fetch_unsynced(self, table_name):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table_name} WHERE synced=FALSE")
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def mark_synced(self, table_name, ids):
        if not ids:
            return
        cursor = self.conn.cursor()
        format_strings = ','.join(['%s'] * len(ids))
        cursor.execute(f"UPDATE {table_name} SET synced=TRUE WHERE id IN ({format_strings})", tuple(ids))
        self.conn.commit()
        cursor.close()
