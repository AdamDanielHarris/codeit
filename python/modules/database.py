#!/usr/bin/env python3
"""
Database Operations and Patterns Module

This module demonstrates database concepts using SQLite for hands-on practice
and intelligent mocks for enterprise database patterns.
"""

import sqlite3
import os
import tempfile
from datetime import datetime, timedelta
import random

def set_context(data_type):
    """Set the current context for cs() function based on data type."""
    global _current_context
    _current_context = data_type

def check_interactive_mode():
    """Placeholder function - will be replaced by main script's version"""
    pass

def step_through_function(func, global_ns=None, local_ns=None):
    """Placeholder function - will be replaced by main script's version"""
    func()

def snippet_section(code_lines, description=None):
    """Placeholder function - will be replaced by main script's version"""
    pass

# SQLite Database Functions (Real Implementation)
def create_security_logs_database():
    """Create a realistic security logs database with sample data"""
    # Create database in a practice directory
    practice_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'practice', 'database')
    os.makedirs(practice_dir, exist_ok=True)
    
    db_path = os.path.join(practice_dir, 'security_logs.db')
    conn = sqlite3.connect(db_path)
    
    # Create security events table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS security_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            source_ip TEXT,
            event_type TEXT,
            severity TEXT,
            description TEXT,
            user_agent TEXT,
            country TEXT
        )
    ''')
    
    # Create users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT,
            created_at DATETIME,
            last_login DATETIME,
            is_active BOOLEAN
        )
    ''')
    
    # Check if data already exists
    cursor = conn.execute('SELECT COUNT(*) FROM security_events')
    if cursor.fetchone()[0] == 0:
        # Generate sample data
        generate_sample_security_data(conn)
    
    return conn

def generate_sample_security_data(conn):
    """Generate realistic sample security data"""
    import random
    from datetime import datetime, timedelta
    
    # Sample data arrays
    event_types = ['login_failed', 'malware_detected', 'port_scan', 'brute_force', 'data_exfiltration', 'unauthorized_access']
    severities = ['low', 'medium', 'high', 'critical']
    countries = ['USA', 'China', 'Russia', 'Germany', 'Brazil', 'India', 'Japan', 'UK']
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'curl/7.68.0',
        'Python-requests/2.25.1',
        'sqlmap/1.4.7'
    ]
    
    # Generate security events
    events = []
    start_date = datetime.now() - timedelta(days=30)
    
    for _ in range(5000):
        timestamp = start_date + timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        # Generate realistic IP addresses
        ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        
        event_type = random.choice(event_types)
        severity = random.choice(severities)
        country = random.choice(countries)
        user_agent = random.choice(user_agents)
        
        # Generate contextual descriptions
        descriptions = {
            'login_failed': f'Failed login attempt for user admin from {ip}',
            'malware_detected': f'Malware signature detected in file upload from {ip}',
            'port_scan': f'Port scanning activity detected from {ip}',
            'brute_force': f'Brute force attack detected against SSH service from {ip}',
            'data_exfiltration': f'Suspicious data transfer detected to {ip}',
            'unauthorized_access': f'Unauthorized access attempt to admin panel from {ip}'
        }
        
        events.append((
            timestamp.isoformat(),
            ip,
            event_type,
            severity,
            descriptions[event_type],
            user_agent,
            country
        ))
    
    # Insert security events
    conn.executemany('''
        INSERT INTO security_events 
        (timestamp, source_ip, event_type, severity, description, user_agent, country)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', events)
    
    # Generate sample users
    users = []
    usernames = ['admin', 'john.doe', 'alice.smith', 'bob.wilson', 'charlie.brown', 'diana.prince']
    
    for i, username in enumerate(usernames):
        created_at = start_date + timedelta(days=random.randint(-365, -30))
        last_login = start_date + timedelta(days=random.randint(0, 30))
        
        users.append((
            username,
            f"{username.replace('.', '')}@company.com",
            created_at.isoformat(),
            last_login.isoformat(),
            random.choice([True, False])
        ))
    
    conn.executemany('''
        INSERT INTO users 
        (username, email, created_at, last_login, is_active)
        VALUES (?, ?, ?, ?, ?)
    ''', users)
    
    conn.commit()

# Mock Database Classes (For Learning Patterns)
class MockPostgreSQLConnection:
    """Mock PostgreSQL connection demonstrating enterprise patterns"""
    
    def __init__(self):
        self.connected = True
        print("🐘 Connected to PostgreSQL (Mock)")
    
    def execute(self, query):
        """Execute SQL and return realistic mock results"""
        query_lower = query.lower().strip()
        
        if 'select count(*) from users' in query_lower:
            return [(1247,)]
        elif 'select * from users' in query_lower and 'limit' in query_lower:
            return [
                (1, 'alice.admin', 'alice@company.com', '2024-01-15', True),
                (2, 'bob.dev', 'bob@company.com', '2024-02-20', True),
                (3, 'charlie.ops', 'charlie@company.com', '2024-03-10', False)
            ]
        elif 'avg' in query_lower and 'performance' in query_lower:
            return [(234.56,)]
        else:
            return [("PostgreSQL mock result for:", query[:50] + "...")]
    
    def close(self):
        print("🐘 PostgreSQL connection closed")

class MockNeo4jDriver:
    """Mock Neo4j driver demonstrating graph database concepts"""
    
    def __init__(self):
        self.connected = True
        print("🕸️  Connected to Neo4j (Mock)")
    
    def session(self):
        return MockNeo4jSession()
    
    def close(self):
        print("🕸️  Neo4j connection closed")

class MockNeo4jSession:
    """Mock Neo4j session"""
    
    def __enter__(self):
        """Support context manager protocol"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support context manager protocol"""
        pass
    
    def run(self, cypher_query):
        """Execute Cypher and return realistic graph results"""
        query_lower = cypher_query.lower()
        
        if 'match (u:user)' in query_lower and 'return u' in query_lower:
            return [
                {"u": {"name": "Alice", "role": "Admin"}},
                {"u": {"name": "Bob", "role": "Developer"}},
                {"u": {"name": "Charlie", "role": "Operations"}}
            ]
        elif 'shortestpath' in query_lower or 'shortest path' in query_lower:
            return [{"path": "Alice -> Bob -> Charlie -> Diana"}]
        elif 'works_with' in query_lower or 'manages' in query_lower:
            return [
                {"user1": "Alice", "user2": "Bob", "relationship": "WORKS_WITH"},
                {"user1": "Bob", "user2": "Charlie", "relationship": "MANAGES"}
            ]
        else:
            return [{"result": f"Neo4j mock result for Cypher query"}]
    
    def close(self):
        pass

class MockRedisClient:
    """Mock Redis client demonstrating caching patterns"""
    
    def __init__(self):
        self.cache = {}
        print("⚡ Connected to Redis (Mock)")
    
    def set(self, key, value, ex=None):
        """Set a key-value pair with optional expiration"""
        self.cache[key] = value
        if ex:
            print(f"⚡ SET {key} = {value} (expires in {ex}s)")
        else:
            print(f"⚡ SET {key} = {value}")
    
    def get(self, key):
        """Get a value by key"""
        value = self.cache.get(key, None)
        print(f"⚡ GET {key} = {value}")
        return value
    
    def exists(self, key):
        """Check if key exists"""
        exists = key in self.cache
        print(f"⚡ EXISTS {key} = {exists}")
        return exists
    
    def delete(self, key):
        """Delete a key"""
        if key in self.cache:
            del self.cache[key]
            print(f"⚡ DEL {key}")
            return 1
        return 0

def database_module(step=False):
    """
    Demonstrates database operations and patterns.
    Uses SQLite for hands-on practice and mocks for enterprise concepts.
    If step=True, drops into interactive shell after every line in this block.
    """
    def database_block():
        set_context('database')
        
        print("🗄️  Database Operations and Patterns")
        print("=" * 60)
        print("This module demonstrates database concepts from basic SQL to enterprise patterns.")
        print("Uses real SQLite databases for hands-on practice and intelligent mocks for learning.")
        print()
        
        check_interactive_mode()
    
    # Section 1: SQLite - Real Database Operations
    print("📊 Section 1: SQLite Database (REAL)")
    print("-" * 40)
    print("Creating and working with a real SQLite database")
    
    # Create the database
    conn = create_security_logs_database()
    print("✅ Security logs database created with sample data")
    
    # Basic SQL queries
    print("\n🔍 Basic SQL Queries:")
    
    # Count total events
    cursor = conn.execute('SELECT COUNT(*) FROM security_events')
    total_events = cursor.fetchone()[0]
    print(f"Total security events: {total_events}")
    
    # Group by severity
    cursor = conn.execute('''
        SELECT severity, COUNT(*) as count 
        FROM security_events 
        GROUP BY severity 
        ORDER BY count DESC
    ''')
    print("\nEvents by severity:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} events")
    
    # Top event types
    cursor = conn.execute('''
        SELECT event_type, COUNT(*) as count 
        FROM security_events 
        GROUP BY event_type 
        ORDER BY count DESC 
        LIMIT 3
    ''')
    print("\nTop 3 event types:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} events")
    
    snippet_section([
        "import sqlite3",
        "",
        "# Connect to SQLite database",
        "conn = sqlite3.connect('practice/database/security_logs.db')",
        "",
        "# Basic query - count all events",
        "cursor = conn.execute('SELECT COUNT(*) FROM security_events')",
        "total = cursor.fetchone()[0]",
        "print(f'Total events: {total}')",
        "",
        "# Group by severity",
        "cursor = conn.execute('''",
        "    SELECT severity, COUNT(*) as count",
        "    FROM security_events",
        "    GROUP BY severity",
        "    ORDER BY count DESC",
        "''')",
        "for row in cursor.fetchall():",
        "    print(f'{row[0]}: {row[1]} events')",
        "",
        "conn.close()"
    ], "Basic SQLite operations")
    
    check_interactive_mode()
    
    # Advanced SQL with JOINs
    print("\n🔗 Advanced SQL - JOIN Operations:")
    
    # Simulate a JOIN (in a real scenario, we might have user_events table)
    cursor = conn.execute('''
        SELECT 
            se.event_type,
            se.severity,
            COUNT(*) as event_count,
            GROUP_CONCAT(DISTINCT se.country) as countries
        FROM security_events se
        WHERE se.timestamp >= date('now', '-7 days')
        GROUP BY se.event_type, se.severity
        HAVING event_count > 10
        ORDER BY event_count DESC
    ''')
    
    print("Recent events (last 7 days) with >10 occurrences:")
    for row in cursor.fetchall():
        countries = row[3][:50] + "..." if len(row[3]) > 50 else row[3]
        print(f"  {row[0]} ({row[1]}): {row[2]} events from {countries}")
    
    snippet_section([
        "# Advanced SQL with aggregation and filtering",
        "cursor = conn.execute('''",
        "    SELECT ",
        "        event_type,",
        "        severity,",
        "        COUNT(*) as event_count,",
        "        GROUP_CONCAT(DISTINCT country) as countries",
        "    FROM security_events",
        "    WHERE timestamp >= date('now', '-7 days')",
        "    GROUP BY event_type, severity",
        "    HAVING event_count > 10",
        "    ORDER BY event_count DESC",
        "''')",
        "",
        "for row in cursor.fetchall():",
        "    print(f'{row[0]} ({row[1]}): {row[2]} events')"
    ], "Advanced SQL queries")
    
    check_interactive_mode()
    
    # Close SQLite connection
    conn.close()
    print("\n✅ SQLite database connection closed")
    
    # Section 2: PostgreSQL Patterns (Mock)
    print("\n🐘 Section 2: PostgreSQL Patterns (DEMO)")
    print("-" * 40)
    print("Demonstrating enterprise PostgreSQL patterns")
    
    # Connection pattern
    pg_conn = MockPostgreSQLConnection()
    
    # Enterprise query patterns
    print("\n📈 Enterprise Query Patterns:")
    
    # Count query
    result = pg_conn.execute("SELECT COUNT(*) FROM users WHERE is_active = true")
    print(f"Active users: {result[0][0]}")
    
    # Pagination query
    result = pg_conn.execute("SELECT * FROM users ORDER BY created_at DESC LIMIT 3 OFFSET 0")
    print("\nRecent users:")
    for row in result:
        print(f"  {row[1]} ({row[2]}) - Active: {row[4]}")
    
    # Performance metrics
    result = pg_conn.execute("SELECT AVG(response_time_ms) FROM performance_metrics WHERE date >= CURRENT_DATE - INTERVAL '7 days'")
    print(f"\nAverage response time (7 days): {result[0][0]:.2f}ms")
    
    snippet_section([
        "import psycopg2",
        "",
        "# PostgreSQL connection pattern",
        "conn = psycopg2.connect(",
        "    host='localhost',",
        "    database='security_db',",
        "    user='security_user',",
        "    password='secure_password'",
        ")",
        "",
        "# Enterprise query with pagination",
        "cursor = conn.cursor()",
        "cursor.execute('''",
        "    SELECT id, username, email, last_login",
        "    FROM users",
        "    WHERE is_active = true",
        "    ORDER BY last_login DESC",
        "    LIMIT 10 OFFSET %s",
        "''', (page * 10,))",
        "",
        "users = cursor.fetchall()",
        "conn.close()"
    ], "PostgreSQL connection and queries")
    
    check_interactive_mode()
    
    pg_conn.close()
    
    # Section 3: Neo4j Graph Database (Mock)
    print("\n🕸️  Section 3: Neo4j Graph Database (DEMO)")
    print("-" * 40)
    print("Demonstrating graph database concepts and relationships")
    
    neo4j_driver = MockNeo4jDriver()
    
    with neo4j_driver.session() as session:
        print("\n👥 User Relationships:")
        
        # Find all users
        result = session.run("MATCH (u:User) RETURN u LIMIT 3")
        for record in result:
            user = record["u"]
            print(f"  {user['name']} - {user['role']}")
        
        print("\n🔗 Relationship Queries:")
        
        # Find connections
        result = session.run("""
            MATCH (u1:User)-[r:WORKS_WITH|MANAGES]-(u2:User)
            RETURN u1.name, type(r), u2.name
        """)
        for record in result:
            print(f"  {record['user1']} --{record['relationship']}--> {record['user2']}")
        
        # Shortest path
        result = session.run("""
            MATCH (alice:User {name: 'Alice'}), (diana:User {name: 'Diana'})
            MATCH path = shortestPath((alice)-[:WORKS_WITH|MANAGES*]-(diana))
            RETURN path
        """)
        for record in result:
            print(f"  Shortest path: {record['path']}")
    
    snippet_section([
        "from neo4j import GraphDatabase",
        "",
        "# Neo4j connection",
        "driver = GraphDatabase.driver(",
        "    'bolt://localhost:7687',",
        "    auth=('neo4j', 'password')",
        ")",
        "",
        "# Graph query with relationships",
        "with driver.session() as session:",
        "    result = session.run('''",
        "        MATCH (u1:User)-[r:WORKS_WITH]-(u2:User)",
        "        WHERE u1.department = 'Security'",
        "        RETURN u1.name, u2.name, r.since",
        "    ''')",
        "    ",
        "    for record in result:",
        "        print(f'{record[\"u1.name\"]} works with {record[\"u2.name\"]}')",
        "",
        "driver.close()"
    ], "Neo4j graph database queries")
    
    check_interactive_mode()
    
    neo4j_driver.close()
    
    # Section 4: Redis Caching (Mock)
    print("\n⚡ Section 4: Redis Caching Patterns (DEMO)")
    print("-" * 40)
    print("Demonstrating caching strategies and patterns")
    
    redis_client = MockRedisClient()
    
    print("\n💾 Caching Patterns:")
    
    # Cache user data
    redis_client.set("user:1001", "{'name': 'Alice', 'role': 'Admin'}", ex=3600)
    redis_client.set("session:abc123", "user:1001", ex=1800)
    
    # Cache hit/miss pattern
    cached_user = redis_client.get("user:1001")
    if cached_user:
        print("✅ Cache hit - user data retrieved from Redis")
    else:
        print("❌ Cache miss - would query database")
    
    # Session management
    session_exists = redis_client.exists("session:abc123")
    print(f"Session valid: {session_exists}")
    
    # Cache invalidation
    redis_client.delete("user:1001")
    print("🗑️  User cache invalidated")
    
    snippet_section([
        "import redis",
        "",
        "# Redis connection",
        "r = redis.Redis(host='localhost', port=6379, db=0)",
        "",
        "# Caching pattern with expiration",
        "def get_user_data(user_id):",
        "    cache_key = f'user:{user_id}'",
        "    ",
        "    # Try cache first",
        "    cached = r.get(cache_key)",
        "    if cached:",
        "        return json.loads(cached)",
        "    ",
        "    # Cache miss - query database",
        "    user_data = query_database(user_id)",
        "    ",
        "    # Cache for 1 hour",
        "    r.setex(cache_key, 3600, json.dumps(user_data))",
        "    return user_data",
        "",
        "# Session management",
        "def create_session(user_id):",
        "    session_id = generate_session_id()",
        "    r.setex(f'session:{session_id}', 1800, user_id)",
        "    return session_id"
    ], "Redis caching patterns")
    
    check_interactive_mode()
    
    # Database Design Principles
    print("\n🏗️  Database Design Principles")
    print("-" * 40)
    print("Key concepts for choosing the right database:")
    print()
    print("📊 Relational (PostgreSQL, MySQL):")
    print("   • ACID transactions")
    print("   • Complex queries with JOINs")
    print("   • Structured data with relationships")
    print("   • Financial systems, user management")
    print()
    print("🕸️  Graph (Neo4j, Amazon Neptune):")
    print("   • Complex relationships")
    print("   • Social networks, recommendation engines")
    print("   • Fraud detection, network analysis")
    print("   • Path finding algorithms")
    print()
    print("⚡ Cache (Redis, Memcached):")
    print("   • High-speed data access")
    print("   • Session storage, API rate limiting")
    print("   • Real-time analytics")
    print("   • Temporary data storage")
    print()
    print("📄 Document (MongoDB, CouchDB):")
    print("   • Flexible schema")
    print("   • JSON-like documents")
    print("   • Content management, catalogs")
    print("   • Rapid prototyping")
    
    check_interactive_mode()
    
    print("\n🎯 Summary: Database Selection Guide")
    print("=" * 50)
    print("Choose your database based on:")
    print("• Data structure (structured vs. unstructured)")
    print("• Relationships (simple vs. complex)")
    print("• Scale requirements (reads vs. writes)")
    print("• Consistency needs (eventual vs. immediate)")
    print("• Query patterns (simple lookups vs. complex analytics)")
    print()
    print("🚀 Practice with the generated SQLite database!")
    print("📁 Location: practice/database/security_logs.db")

    if step:
        step_through_function(database_block, globals(), locals())
    else:
        database_block()

# Module metadata
DESCRIPTION = 'Database Operations and Patterns'
FUNCTION = database_module
