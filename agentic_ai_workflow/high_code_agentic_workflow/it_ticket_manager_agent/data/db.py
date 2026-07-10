from __future__ import annotations
import sqlite3
import os
import json
from typing import Optional
from core.models import Ticket, TicketCategory, TicketEvent, TicketPriority, TicketStatus
from core.interfaces import ITicketRepository
from datetime import datetime
from config import DB_PATH


class SqlDBManager(ITicketRepository):
    
    def __init__(self, db_name):
        
        # connection
        self.db_name=db_name
        os.makedirs(os.path.dirname(db_name), exist_ok=True)
        
    def _get_connection(self)->sqlite3.Connection:
        conn = sqlite3.connect(self.db_name)
        # get cursor
        conn.row_factory = sqlite3.Row
        return conn
        
    def _init_db(self)->None:
        conn = self._get_connection()
        
        try:
            conn.executescript("""
                            CREATE TABLE IF NOT EXISTS tickets (
                            id TEXT PRIMARY KEY,
                            title TEXT NOT NULL,
                            description TEXT NOT NULL,
                            category TEXT NOT NULL,
                            status TEXT NOT ONLY,
                            priority TEXT NOT ONLY,
                            created_at TEXT NOT ONLY,
                            updated_at TEXT NOT NULL,
                            resolved_at TEXT
                            );
                            CREATE TABLE IF NOT EXISTS ticket_events(
                                id INTEGER PRIMARY KEY  AUTOINCREMENT,
                                ticket_id  TEXT NOT NULL,
                                event_type TEXT NOT NULL,
                                description TEXT NOT NULL,   
                                agent TEXT NOT NULL,
                                FOREIGN KEY (ticket_id) REFERENCES tickets(id)   
                            )
                            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Create Table {e}")
            conn.close()
            
    def insert_ticket(self, ticket:Ticket)->Ticket:
        
        conn = self._get_connection()

        conn.execute("""
                        INSERT INTO tickets (id, title, description, category, status, priority,
                        assigned_to, created_at, updated_at, resolved_at, resolution)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,(
                            ticket.id,
                            ticket.title,
                            ticket.description,
                            ticket.category.value,
                            ticket.status.value,
                            ticket.priority.value,
                            ticket.created_at.isoformat(),
                            ticket.updated_at.isoformat(),
                            ticket.resolved_at.isoformat() if ticket.resolved_at else None,
                        ))

        conn.commit()
        conn.close()
        return self.get_ticket(ticket.id)
    
    def get_ticket(self, ticket_id:str)->Optional[Ticket]:
        conn = self._get_connection()
        row = conn.execute(
            "SELECT * FROM tickets where id=?", (ticket_id,)
        ).fetchone()
        conn.close()
    
        if not row:
            return None
        return Ticket(
            id = row['id'],
            title=row['title'],
            description=row["description"],
            category=TicketCategory(row["category"]),
            status=TicketStatus(row["status"]),
            priority=TicketPriority(row["priority"]),
            assigned_to=row["assigned_to"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            resolved_at=datetime.fromisoformat(row["resolved_at"]) if row["resolved_at"] else None,
            resolution=row["resolution"],
        )
    
    
    ########################################################
    ### UPDATE ###
    #########################################################
    def update_ticket(self, ticket_id: str, **fields) -> Ticket:
        fields["updated_at"] = datetime.now().isoformat()
        set_clause = ", ".join(f"{k} = ?" for k in fields)
        values = [
            v.value if hasattr(v, "value") else v
            for v in fields.values()
        ] + [ticket_id]
        conn = self._get_connection()
        conn.execute(
            f"UPDATE tickets SET {set_clause} WHERE id = ?", values
        )
        conn.commit()
        conn.close()
        return self.get_ticket(ticket_id)
    
    ###########################################################3
    #########################################################3
    def list_all_tickets(self)->list[Ticket]:
        
        conn = self._get_connection()
        rows = conn.execute(
            "SELECT * FROM status != 'resolved' ORDER BY created_at DESC"
        ).fetchall()
        conn.close()
        return [for row in rows]