#!/usr/bin/env python3
"""
Advanced Programming Challenges Module

This module contains more advanced algorithmic challenges focusing on:
- System design patterns
- Data processing and optimization
- Cloud security related problems
- Production-ready code practices
- Database optimization scenarios
"""

def set_context(data_type):
    """Set the current context for cs() function based on data type."""
    global _current_context
    _current_context = data_type

# Import required libraries at module level
from collections import deque, defaultdict
import time
import threading
import json
from typing import List, Dict, Optional, Any
import heapq

def check_interactive_mode():
    """Placeholder function - will be replaced by main script's version"""
    pass

def step_through_function(func, global_ns=None, local_ns=None):
    """Placeholder function - will be replaced by main script's version"""
    func()

def snippet_section(code_lines, description=None):
    """Placeholder function - will be replaced by main script's version"""
    pass

# Production-ready classes available in interactive mode

class SlidingWindowRateLimiter:
    """
    Sliding window rate limiter for API endpoints.
    Useful for cloud security and API management.
    """
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = deque()
    
    def allow_request(self):
        now = time.time()
        # Remove old requests outside the window
        while self.requests and self.requests[0] <= now - self.window_seconds:
            self.requests.popleft()
        
        # Check if we can allow this request
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False
    
    def get_current_usage(self):
        """Get current number of requests in the window"""
        now = time.time()
        while self.requests and self.requests[0] <= now - self.window_seconds:
            self.requests.popleft()
        return len(self.requests)
    
    def get_stats(self):
        """Get detailed statistics about the rate limiter"""
        now = time.time()
        # Clean old requests first
        while self.requests and self.requests[0] <= now - self.window_seconds:
            self.requests.popleft()
        return {
            'current_requests': len(self.requests),
            'max_requests': self.max_requests,
            'window_seconds': self.window_seconds,
            'requests_available': self.max_requests - len(self.requests),
            'usage_percentage': (len(self.requests) / self.max_requests) * 100 if self.max_requests > 0 else 0
        }

class LRUCache:
    """
    Least Recently Used Cache implementation.
    Common in system design interviews and production systems.
    """
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.order = deque()
    
    def get(self, key):
        if key in self.cache:
            # Move to end (most recently used)
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return None
    
    def put(self, key, value):
        if key in self.cache:
            # Update existing
            self.cache[key] = value
            self.order.remove(key)
            self.order.append(key)
        else:
            # Add new
            if len(self.cache) >= self.capacity:
                # Remove least recently used
                oldest = self.order.popleft()
                del self.cache[oldest]
            
            self.cache[key] = value
            self.order.append(key)

class CircuitBreaker:
    """
    Circuit breaker pattern for resilient systems.
    Essential for microservices and cloud applications.
    """
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = 'HALF_OPEN'
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
            
            raise e

# Challenge functions for production-ready scenarios

def rate_limiter_sliding_window(max_requests, window_seconds):
    """
    Demonstrates sliding window rate limiter implementation.
    Useful for API rate limiting in cloud services.
    """
    print(f"Creating rate limiter: {max_requests} requests per {window_seconds} seconds")
    
    # Create an instance
    limiter = SlidingWindowRateLimiter(max_requests, window_seconds)
    
    # Demonstrate usage
    print("Testing rate limiter...")
    for i in range(max_requests + 2):
        allowed = limiter.allow_request()
        current_usage = limiter.get_current_usage()
        print(f"Request {i+1}: {'✓ Allowed' if allowed else '✗ Denied'} (usage: {current_usage}/{max_requests})")
        
        if i == max_requests - 1:
            print("Reached limit, next requests should be denied...")
    
    return limiter

def log_analyzer(log_entries):
    """
    Analyzes log entries for security patterns and anomalies.
    Simulates cloud security event processing.
    """
    from collections import defaultdict, Counter
    import re
    from datetime import datetime
    
    # Parse log entries and extract patterns
    patterns = {
        'failed_login': re.compile(r'Failed login.*from (\d+\.\d+\.\d+\.\d+)'),
        'sql_injection': re.compile(r'(union|select|drop|insert).*--', re.IGNORECASE),
        'unusual_access': re.compile(r'access from (\d+\.\d+\.\d+\.\d+).*at (\d{2}:\d{2})'),
        'large_data_transfer': re.compile(r'transferred (\d+)MB')
    }
    
    analysis = {
        'failed_logins': defaultdict(int),
        'sql_injection_attempts': [],
        'unusual_access_times': [],
        'large_transfers': [],
        'ip_frequency': Counter(),
        'total_events': len(log_entries)
    }
    
    for entry in log_entries:
        # Check for failed logins
        if match := patterns['failed_login'].search(entry):
            ip = match.group(1)
            analysis['failed_logins'][ip] += 1
            analysis['ip_frequency'][ip] += 1
        
        # Check for SQL injection attempts
        if patterns['sql_injection'].search(entry):
            analysis['sql_injection_attempts'].append(entry)
        
        # Check for unusual access times (late night/early morning)
        if match := patterns['unusual_access'].search(entry):
            ip, time_str = match.groups()
            hour = int(time_str.split(':')[0])
            if hour < 6 or hour > 22:  # Outside business hours
                analysis['unusual_access_times'].append((ip, time_str, entry))
        
        # Check for large data transfers
        if match := patterns['large_data_transfer'].search(entry):
            size_mb = int(match.group(1))
            if size_mb > 100:  # Threshold for "large"
                analysis['large_transfers'].append((size_mb, entry))
    
    return analysis

def cloud_resource_optimizer(resources):
    """
    Optimizes cloud resource allocation using a greedy algorithm.
    Similar to problems faced in cloud security platforms.
    """
    # Sort resources by efficiency ratio (value/cost)
    sorted_resources = sorted(
        resources, 
        key=lambda x: x['value'] / x['cost'] if x['cost'] > 0 else float('inf'), 
        reverse=True
    )
    
    def optimize_for_budget(budget):
        selected = []
        total_cost = 0
        total_value = 0
        
        for resource in sorted_resources:
            if total_cost + resource['cost'] <= budget:
                selected.append(resource)
                total_cost += resource['cost']
                total_value += resource['value']
        
        return {
            'selected_resources': selected,
            'total_cost': total_cost,
            'total_value': total_value,
            'efficiency': total_value / total_cost if total_cost > 0 else 0,
            'budget_utilization': (total_cost / budget) * 100 if budget > 0 else 0
        }
    
    return optimize_for_budget

def event_stream_processor():
    """
    Processes streaming events with batching and deduplication.
    Simulates real-time security event processing.
    """
    class EventProcessor:
        def __init__(self, batch_size=100, dedup_window=300):
            self.batch_size = batch_size
            self.dedup_window = dedup_window  # seconds
            self.current_batch = []
            self.processed_events = {}  # event_id -> timestamp
            self.total_processed = 0
            self.total_duplicates = 0
        
        def process_event(self, event):
            import time
            import hashlib
            
            # Create event fingerprint for deduplication
            event_data = f"{event.get('source', '')}{event.get('type', '')}{event.get('data', '')}"
            event_id = hashlib.md5(event_data.encode()).hexdigest()
            
            current_time = time.time()
            
            # Check for duplicates within the window
            if event_id in self.processed_events:
                last_seen = self.processed_events[event_id]
                if current_time - last_seen < self.dedup_window:
                    self.total_duplicates += 1
                    return {'status': 'duplicate', 'event_id': event_id}
            
            # Add timestamp and event_id to the event
            event['processed_time'] = current_time
            event['event_id'] = event_id
            
            # Add to current batch
            self.current_batch.append(event)
            self.processed_events[event_id] = current_time
            
            # Check if batch is full
            if len(self.current_batch) >= self.batch_size:
                return self.flush_batch()
            
            return {'status': 'queued', 'batch_size': len(self.current_batch)}
        
        def flush_batch(self):
            if not self.current_batch:
                return {'status': 'no_data', 'processed': 0}
            
            batch_size = len(self.current_batch)
            self.total_processed += batch_size
            
            # Simulate batch processing
            processed_batch = list(self.current_batch)
            self.current_batch = []
            
            return {
                'status': 'processed',
                'batch_size': batch_size,
                'total_processed': self.total_processed,
                'total_duplicates': self.total_duplicates,
                'events': processed_batch
            }
        
        def get_stats(self):
            return {
                'current_batch_size': len(self.current_batch),
                'total_processed': self.total_processed,
                'total_duplicates': self.total_duplicates,
                'dedup_efficiency': (self.total_duplicates / (self.total_processed + self.total_duplicates)) * 100 
                                  if (self.total_processed + self.total_duplicates) > 0 else 0
            }
    
    return EventProcessor

def database_query_optimizer():
    """
    Simulates database query optimization scenarios.
    Demonstrates thinking about performance and indexing.
    """
    class QueryOptimizer:
        def __init__(self):
            self.query_plans = {}
            self.execution_stats = {}
        
        def analyze_query(self, query, table_stats):
            """
            Analyzes a query and suggests optimizations.
            
            Args:
                query: SQL-like query string
                table_stats: Dict with table information (row_count, indexes, etc.)
            """
            suggestions = []
            estimated_cost = 0
            
            # Simple pattern matching for common optimization opportunities
            query_lower = query.lower()
            
            # Check for missing WHERE clause on large tables
            if 'select' in query_lower and 'where' not in query_lower:
                for table, stats in table_stats.items():
                    if table.lower() in query_lower and stats.get('row_count', 0) > 10000:
                        suggestions.append(f"Consider adding WHERE clause for table {table} ({stats['row_count']} rows)")
                        estimated_cost += stats['row_count'] * 0.1
            
            # Check for potential index usage
            if 'where' in query_lower:
                # Extract potential column references (simplified)
                import re
                where_clause = query_lower.split('where')[1].split('order by')[0] if 'order by' in query_lower else query_lower.split('where')[1]
                potential_columns = re.findall(r'(\w+)\s*[=<>]', where_clause)
                
                for table, stats in table_stats.items():
                    if table.lower() in query_lower:
                        indexed_columns = stats.get('indexes', [])
                        for col in potential_columns:
                            if col not in indexed_columns:
                                suggestions.append(f"Consider adding index on {table}.{col}")
                                estimated_cost += stats.get('row_count', 1000) * 0.01
                            else:
                                estimated_cost += 10  # Index lookup cost
            
            # Check for JOIN optimizations
            join_count = query_lower.count('join')
            if join_count > 2:
                suggestions.append(f"Query has {join_count} joins - consider query restructuring or materialized views")
                estimated_cost *= (join_count * 1.5)
            
            # Check for SELECT * usage
            if 'select *' in query_lower:
                suggestions.append("Avoid SELECT * - specify only needed columns")
                estimated_cost *= 1.3
            
            return {
                'query': query,
                'estimated_cost': round(estimated_cost, 2),
                'suggestions': suggestions,
                'complexity': 'HIGH' if estimated_cost > 1000 else 'MEDIUM' if estimated_cost > 100 else 'LOW'
            }
        
        def suggest_index(self, table, columns, query_patterns):
            """Suggests optimal index strategy for given query patterns."""
            if isinstance(columns, str):
                columns = [columns]
            
            # Analyze query patterns to suggest index type
            suggestions = []
            
            for pattern in query_patterns:
                pattern_lower = pattern.lower()
                if any(col.lower() in pattern_lower for col in columns):
                    if 'range' in pattern_lower or 'between' in pattern_lower:
                        suggestions.append(f"B-tree index on {', '.join(columns)} for range queries")
                    elif 'in (' in pattern_lower:
                        suggestions.append(f"Hash index on {', '.join(columns)} for equality lookups")
                    elif 'like' in pattern_lower:
                        suggestions.append(f"Text search index on {', '.join(columns)} for pattern matching")
            
            return {
                'table': table,
                'columns': columns,
                'suggested_indexes': suggestions,
                'composite_index': len(columns) > 1
            }
    
    return QueryOptimizer

def challenges_2_module(step=False):
    """
    Demonstrates advanced programming challenges focusing on production scenarios.
    Covers system design, optimization, and cloud security related problems.
    If step=True, drops into interactive shell after every line in this block.
    """
    def challenges_block():
        set_context('challenges_2')
        
        print("🚀 Advanced Programming Challenges")
        print("=" * 60)
        print("This module contains advanced challenges focusing on production scenarios:")
        print("• System design patterns")
        print("• Cloud security event processing")
        print("• Database optimization")
        print("• Rate limiting and streaming data")
        print()
        
        check_interactive_mode()
    
    if step:
        step_through_function(challenges_block, globals(), locals())
    else:
        challenges_block()
    
    # Challenge 1: Rate Limiting for Cloud APIs
    print("🌐 Challenge 1: Sliding Window Rate Limiter")
    print("-" * 45)
    print("Implement rate limiting for cloud API endpoints")
    
    # Create a rate limiter: 5 requests per 10 seconds
    limiter = rate_limiter_sliding_window(5, 10)
    
    print("Testing rate limiter (5 requests per 10 seconds):")
    
    # Simulate API requests
    import time
    for i in range(8):
        allowed = limiter.allow_request()
        stats = limiter.get_stats()
        print(f"Request {i+1}: {'✅ ALLOWED' if allowed else '❌ REJECTED'} "
              f"({stats['current_requests']}/{stats['max_requests']} used)")
        if i == 4:  # Pause to show sliding window effect
            print("   Waiting 2 seconds...")
            time.sleep(2)
    
    snippet_section([
        "# Sliding Window Rate Limiter Implementation",
        "",
        "from collections import deque",
        "import time",
        "",
        "class SlidingWindowRateLimiter:",
        "    def __init__(self, max_requests, window_seconds):",
        "        self.max_requests = max_requests",
        "        self.window_seconds = window_seconds",
        "        self.requests = deque()",
        "    ",
        "    def allow_request(self):",
        "        now = time.time()",
        "        # Remove old requests outside the window",
        "        while self.requests and self.requests[0] <= now - self.window_seconds:",
        "            self.requests.popleft()",
        "        ",
        "        # Check if we can allow this request",
        "        if len(self.requests) < self.max_requests:",
        "            self.requests.append(now)",
        "            return True",
        "        return False",
        "",
        "# Usage example",
        "limiter = SlidingWindowRateLimiter(5, 10)  # 5 requests per 10 seconds",
        "allowed = limiter.allow_request()",
        "print(f'Request allowed: {allowed}')"
    ], "Sliding window rate limiter for API endpoints")
    
    check_interactive_mode()
    
    # Challenge 2: Security Log Analysis
    print("\n🔒 Challenge 2: Security Log Analyzer")
    print("-" * 40)
    print("Analyze security logs for threats and anomalies")
    
    # Sample security log entries
    sample_logs = [
        "2024-01-15 14:30:22 Failed login attempt from 192.168.1.100",
        "2024-01-15 14:30:25 Failed login attempt from 192.168.1.100",
        "2024-01-15 14:30:28 Failed login attempt from 192.168.1.100",
        "2024-01-15 02:15:33 Unusual access from 10.0.0.5 at 02:15",
        "2024-01-15 15:45:12 SQL query: SELECT * FROM users WHERE id=1 UNION SELECT password FROM admin_users --",
        "2024-01-15 16:20:45 File transfer: transferred 250MB from server to 203.0.113.0",
        "2024-01-15 23:30:15 Late night access from 172.16.0.10 at 23:30",
        "2024-01-15 17:00:00 Normal login from 192.168.1.50"
    ]
    
    analysis = log_analyzer(sample_logs)
    
    print(f"📊 Log Analysis Results:")
    print(f"   Total events processed: {analysis['total_events']}")
    print(f"   Failed login attempts: {len(analysis['failed_logins'])} unique IPs")
    
    for ip, count in analysis['failed_logins'].items():
        print(f"      • {ip}: {count} attempts")
    
    print(f"   SQL injection attempts: {len(analysis['sql_injection_attempts'])}")
    for attempt in analysis['sql_injection_attempts']:
        print(f"      • {attempt[:80]}...")
    
    print(f"   Unusual access times: {len(analysis['unusual_access_times'])}")
    for ip, time_str, entry in analysis['unusual_access_times']:
        print(f"      • {ip} at {time_str}")
    
    print(f"   Large data transfers: {len(analysis['large_transfers'])}")
    for size, entry in analysis['large_transfers']:
        print(f"      • {size}MB transfer detected")
    
    snippet_section([
        "# Security Log Analysis with Pattern Matching",
        "",
        "import re",
        "from collections import defaultdict, Counter",
        "",
        "def analyze_security_logs(log_entries):",
        "    patterns = {",
        "        'failed_login': re.compile(r'Failed login.*from (\\d+\\.\\d+\\.\\d+\\.\\d+)'),",
        "        'sql_injection': re.compile(r'(union|select|drop|insert).*--', re.IGNORECASE),",
        "        'unusual_access': re.compile(r'access from (\\d+\\.\\d+\\.\\d+\\.\\d+).*at (\\d{2}:\\d{2})')",
        "    }",
        "    ",
        "    analysis = {",
        "        'failed_logins': defaultdict(int),",
        "        'sql_injection_attempts': [],",
        "        'unusual_access_times': []",
        "    }",
        "    ",
        "    for entry in log_entries:",
        "        # Check each pattern and collect matches",
        "        if match := patterns['failed_login'].search(entry):",
        "            ip = match.group(1)",
        "            analysis['failed_logins'][ip] += 1",
        "    ",
        "    return analysis",
        "",
        "# Usage",
        "logs = ['2024-01-15 14:30:22 Failed login attempt from 192.168.1.100']",
        "results = analyze_security_logs(logs)",
        "print(f'Failed logins: {dict(results[\"failed_logins\"])}')"
    ], "Security log analysis with regex patterns")
    
    check_interactive_mode()
    
    # Challenge 3: Cloud Resource Optimization
    print("\n☁️ Challenge 3: Cloud Resource Optimizer")
    print("-" * 42)
    print("Optimize cloud resource allocation within budget constraints")
    
    # Sample cloud resources with cost and value
    cloud_resources = [
        {'name': 'High-CPU Instance', 'cost': 100, 'value': 150, 'type': 'compute'},
        {'name': 'GPU Instance', 'cost': 200, 'value': 350, 'type': 'compute'},
        {'name': 'Storage Cluster', 'cost': 50, 'value': 80, 'type': 'storage'},
        {'name': 'Load Balancer', 'cost': 30, 'value': 60, 'type': 'network'},
        {'name': 'Database Instance', 'cost': 150, 'value': 200, 'type': 'database'},
        {'name': 'Cache Cluster', 'cost': 75, 'value': 120, 'type': 'cache'},
        {'name': 'Monitoring Service', 'cost': 25, 'value': 50, 'type': 'monitoring'}
    ]
    
    optimizer = cloud_resource_optimizer(cloud_resources)
    budget = 300
    
    result = optimizer(budget)
    
    print(f"💰 Budget Optimization Results (Budget: ${budget}):")
    print(f"   Selected {len(result['selected_resources'])} resources")
    print(f"   Total cost: ${result['total_cost']} ({result['budget_utilization']:.1f}% of budget)")
    print(f"   Total value: {result['total_value']}")
    print(f"   Efficiency ratio: {result['efficiency']:.2f}")
    print()
    print("   Selected resources:")
    for resource in result['selected_resources']:
        efficiency = resource['value'] / resource['cost']
        print(f"      • {resource['name']}: ${resource['cost']} → {resource['value']} value (ratio: {efficiency:.2f})")
    
    snippet_section([
        "# Cloud Resource Optimization Algorithm",
        "",
        "def optimize_cloud_resources(resources, budget):",
        "    # Sort by value-to-cost ratio (greedy approach)",
        "    sorted_resources = sorted(",
        "        resources,",
        "        key=lambda x: x['value'] / x['cost'],",
        "        reverse=True",
        "    )",
        "    ",
        "    selected = []",
        "    total_cost = 0",
        "    total_value = 0",
        "    ",
        "    for resource in sorted_resources:",
        "        if total_cost + resource['cost'] <= budget:",
        "            selected.append(resource)",
        "            total_cost += resource['cost']",
        "            total_value += resource['value']",
        "    ",
        "    return {",
        "        'selected': selected,",
        "        'total_cost': total_cost,",
        "        'total_value': total_value,",
        "        'efficiency': total_value / total_cost",
        "    }",
        "",
        "# Example usage",
        "resources = [",
        "    {'name': 'GPU Instance', 'cost': 200, 'value': 350},",
        "    {'name': 'Storage', 'cost': 50, 'value': 80}",
        "]",
        "result = optimize_cloud_resources(resources, 300)",
        "print(f'Optimized selection: {len(result[\"selected\"])} resources')"
    ], "Greedy algorithm for cloud resource optimization")
    
    check_interactive_mode()
    
    # Challenge 4: Event Stream Processing
    print("\n📡 Challenge 4: Event Stream Processor")
    print("-" * 40)
    print("Process streaming security events with batching and deduplication")
    
    # Create an instance of the EventProcessor
    processor_class = event_stream_processor()
    processor = processor_class(batch_size=5, dedup_window=300)  # Create instance with smaller batch for demo
    
    # Sample security events
    sample_events = [
        {'source': 'aws-cloudtrail', 'type': 'login', 'data': 'user123@company.com'},
        {'source': 'gcp-audit', 'type': 'resource_access', 'data': 'bucket-read'},
        {'source': 'aws-cloudtrail', 'type': 'login', 'data': 'user123@company.com'},  # Duplicate
        {'source': 'azure-activity', 'type': 'vm_start', 'data': 'vm-prod-01'},
        {'source': 'aws-vpc', 'type': 'network_flow', 'data': '10.0.1.5->10.0.2.10:443'},
    ]
    
    print("Processing events:")
    for i, event in enumerate(sample_events):
        result = processor.process_event(event)
        status_icon = "🔄" if result['status'] == 'queued' else "⚡" if result['status'] == 'processed' else "🔁"
        print(f"   Event {i+1}: {status_icon} {result['status'].upper()}")
        
        if result['status'] == 'duplicate':
            print(f"      └─ Duplicate detected: {result['event_id'][:8]}...")
        elif result['status'] == 'processed':
            print(f"      └─ Batch processed: {result['batch_size']} events")
    
    # Force flush remaining events
    final_result = processor.flush_batch()
    if final_result['status'] == 'processed':
        print(f"   Final flush: ⚡ PROCESSED {final_result['batch_size']} remaining events")
    
    stats = processor.get_stats()
    print(f"\n📈 Processing Statistics:")
    print(f"   Total processed: {stats['total_processed']} events")
    print(f"   Total duplicates: {stats['total_duplicates']} events")
    print(f"   Deduplication efficiency: {stats['dedup_efficiency']:.1f}%")
    
    snippet_section([
        "# Event Stream Processor with Deduplication",
        "",
        "import hashlib",
        "import time",
        "",
        "class EventProcessor:",
        "    def __init__(self, batch_size=100, dedup_window=300):",
        "        self.batch_size = batch_size",
        "        self.dedup_window = dedup_window  # seconds",
        "        self.current_batch = []",
        "        self.processed_events = {}  # event_id -> timestamp",
        "    ",
        "    def process_event(self, event):",
        "        # Create fingerprint for deduplication",
        "        event_data = f\"{event.get('source', '')}{event.get('type', '')}{event.get('data', '')}\"",
        "        event_id = hashlib.md5(event_data.encode()).hexdigest()",
        "        ",
        "        current_time = time.time()",
        "        ",
        "        # Check for duplicates within the window",
        "        if event_id in self.processed_events:",
        "            last_seen = self.processed_events[event_id]",
        "            if current_time - last_seen < self.dedup_window:",
        "                return {'status': 'duplicate'}",
        "        ",
        "        # Add to batch",
        "        self.current_batch.append(event)",
        "        self.processed_events[event_id] = current_time",
        "        ",
        "        # Process batch when full",
        "        if len(self.current_batch) >= self.batch_size:",
        "            return self.flush_batch()",
        "        ",
        "        return {'status': 'queued'}",
        "",
        "# Usage",
        "processor = EventProcessor(batch_size=5, dedup_window=300)",
        "event = {'source': 'aws', 'type': 'login', 'data': 'user@company.com'}",
        "result = processor.process_event(event)",
        "print(f'Event status: {result[\"status\"]}')"
    ], "Streaming event processor with batching and deduplication")
    
    check_interactive_mode()
    
    # Challenge 5: Database Query Optimization
    print("\n🗃️ Challenge 5: Database Query Optimizer")
    print("-" * 42)
    print("Analyze and optimize database queries for performance")
    
    # Create an instance of the QueryOptimizer
    optimizer_class = database_query_optimizer()
    optimizer = optimizer_class()
    
    # Sample table statistics
    table_stats = {
        'security_events': {
            'row_count': 1000000,
            'indexes': ['timestamp', 'event_type'],
            'size_mb': 500
        },
        'users': {
            'row_count': 50000,
            'indexes': ['user_id', 'email'],
            'size_mb': 25
        },
        'audit_logs': {
            'row_count': 5000000,
            'indexes': ['created_at'],
            'size_mb': 1200
        }
    }
    
    # Sample queries to analyze
    sample_queries = [
        "SELECT * FROM security_events WHERE source_ip = '192.168.1.100'",
        "SELECT user_id, event_type FROM security_events JOIN users ON security_events.user_id = users.user_id WHERE created_at > '2024-01-01'",
        "SELECT * FROM audit_logs",  # No WHERE clause on large table
        "SELECT COUNT(*) FROM security_events WHERE event_type = 'login' AND severity > 5"
    ]
    
    print("Query Analysis Results:")
    for i, query in enumerate(sample_queries):
        print(f"\n   Query {i+1}: {query[:50]}...")
        analysis = optimizer.analyze_query(query, table_stats)
        
        complexity_color = "🔴" if analysis['complexity'] == 'HIGH' else "🟡" if analysis['complexity'] == 'MEDIUM' else "🟢"
        print(f"   Complexity: {complexity_color} {analysis['complexity']} (Cost: {analysis['estimated_cost']})")
        
        if analysis['suggestions']:
            print("   Suggestions:")
            for suggestion in analysis['suggestions']:
                print(f"      • {suggestion}")
        else:
            print("   ✅ Query looks optimized!")
    
    # Index suggestion example
    print("\n🔍 Index Optimization Suggestions:")
    index_suggestion = optimizer.suggest_index(
        'security_events', 
        ['source_ip', 'event_type'], 
        ['WHERE source_ip = ?', 'WHERE event_type IN (?, ?, ?)']
    )
    
    print(f"   Table: {index_suggestion['table']}")
    print(f"   Columns: {', '.join(index_suggestion['columns'])}")
    print(f"   Composite index: {'Yes' if index_suggestion['composite_index'] else 'No'}")
    print("   Suggested indexes:")
    for suggestion in index_suggestion['suggested_indexes']:
        print(f"      • {suggestion}")
    
    snippet_section([
        "# Database Query Optimization Analysis",
        "",
        "import re",
        "",
        "def analyze_query_performance(query, table_stats):",
        "    suggestions = []",
        "    estimated_cost = 0",
        "    query_lower = query.lower()",
        "    ",
        "    # Check for missing WHERE clause on large tables",
        "    if 'select' in query_lower and 'where' not in query_lower:",
        "        for table, stats in table_stats.items():",
        "            if table.lower() in query_lower and stats.get('row_count', 0) > 10000:",
        "                suggestions.append(f'Consider adding WHERE clause for {table}')",
        "                estimated_cost += stats['row_count'] * 0.1",
        "    ",
        "    # Check for SELECT * usage",
        "    if 'select *' in query_lower:",
        "        suggestions.append('Avoid SELECT * - specify only needed columns')",
        "        estimated_cost *= 1.3",
        "    ",
        "    # Analyze JOIN complexity",
        "    join_count = query_lower.count('join')",
        "    if join_count > 2:",
        "        suggestions.append(f'Query has {join_count} joins - consider optimization')",
        "        estimated_cost *= (join_count * 1.5)",
        "    ",
        "    return {",
        "        'estimated_cost': round(estimated_cost, 2),",
        "        'suggestions': suggestions,",
        "        'complexity': 'HIGH' if estimated_cost > 1000 else 'MEDIUM' if estimated_cost > 100 else 'LOW'",
        "    }",
        "",
        "# Usage",
        "table_stats = {'events': {'row_count': 1000000, 'indexes': ['timestamp']}}",
        "query = 'SELECT * FROM events'",
        "analysis = analyze_query_performance(query, table_stats)",
        "print(f'Query complexity: {analysis[\"complexity\"]}')",
        "print(f'Suggestions: {analysis[\"suggestions\"]}')"
    ], "Database query performance analysis and optimization")
    
    check_interactive_mode()
    
    print("\n🎯 Advanced Challenges Summary")
    print("=" * 50)
    print("You've completed advanced programming challenges covering:")
    print("✅ Rate limiting for cloud APIs (sliding window algorithm)")
    print("✅ Security log analysis with pattern matching")
    print("✅ Cloud resource optimization (greedy algorithm)")
    print("✅ Event stream processing with deduplication")
    print("✅ Database query optimization and analysis")
    print()
    print("💡 These challenges demonstrate:")
    print("   • Production-ready coding patterns")
    print("   • System design thinking")
    print("   • Performance optimization techniques")
    print("   • Security-focused problem solving")
    print("   • Scalable architecture patterns")
    print()
    print("🚀 Great preparation for technical interviews at cloud security companies!")

# Module exports required by the main script
DESCRIPTION = 'Advanced Programming Challenges - Production Scenarios'
FUNCTION = challenges_2_module
