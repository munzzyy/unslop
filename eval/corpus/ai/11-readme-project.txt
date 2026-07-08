# DataSync

**A lightweight, event-driven data sync engine for Node.js applications.**

DataSync handles incremental synchronization of data between a source and destination database with minimal configuration. It's built for systems that need to keep multiple data stores in sync without managing complex orchestration logic.

## Features

- **Incremental sync.** Only syncs records that have changed since the last run. Uses timestamps or event logs to detect changes.
- **Pluggable adapters.** Built-in support for PostgreSQL, MongoDB, and Redis. Add custom adapters for other datastores.
- **Conflict resolution.** Configurable strategies for handling conflicts (last-write-wins, manual review, merge logic).
- **Dead-letter queue.** Failed syncs are captured in a queue for inspection and replay.
- **Monitoring.** Built-in metrics for sync latency, error rates, and row counts.

## Installation

```bash
npm install datasync
```

## Quick Start

```javascript
const DataSync = require('datasync');

const sync = new DataSync({
  source: {
    type: 'postgres',
    connection: process.env.SOURCE_DB_URL
  },
  destination: {
    type: 'postgres',
    connection: process.env.DEST_DB_URL
  },
  tables: [
    { name: 'users', primaryKey: 'id', syncKey: 'updated_at' },
    { name: 'posts', primaryKey: 'id', syncKey: 'updated_at' }
  ]
});

// Run sync
sync.run().then(result => {
  console.log(`Synced ${result.rowsProcessed} rows`);
}).catch(err => {
  console.error('Sync failed:', err);
});
```

## Configuration

### Basic Options

- **source** (object): Source database connection config
- **destination** (object): Destination database connection config
- **tables** (array): Array of table definitions to sync
  - **name** (string): Table name
  - **primaryKey** (string): Primary key column
  - **syncKey** (string): Timestamp or version column for detecting changes
  - **transform** (function, optional): Custom transformation function applied before write

### Sync Strategies

```javascript
// Timestamp-based (watches for updated_at changes)
{ name: 'users', primaryKey: 'id', syncKey: 'updated_at' }

// Event log-based (syncs from a change log table)
{
  name: 'users',
  primaryKey: 'id',
  changeLog: 'user_changes',
  changeLogTimestamp: 'created_at'
}

// Full table (use with caution on large tables)
{ name: 'users', primaryKey: 'id', fullSync: true }
```

### Conflict Resolution

```javascript
const sync = new DataSync({
  // ... other config
  conflictResolution: 'last-write-wins', // or 'skip', or custom function
  conflictResolutionFn: (source, dest, meta) => {
    // Custom logic to merge or select record
    return source.version > dest.version ? source : dest;
  }
});
```

## API

### sync.run()

Executes a full sync cycle.

```javascript
const result = await sync.run();
// {
//   success: true,
//   rowsProcessed: 1250,
//   rowsInserted: 320,
//   rowsUpdated: 850,
//   rowsDeleted: 80,
//   duration: 4200, // milliseconds
//   errors: []
// }
```

### sync.watch()

Starts continuous sync, polling at intervals.

```javascript
sync.watch({ interval: 60000 }); // Poll every 60 seconds

sync.on('sync-complete', (result) => {
  console.log(`Synced ${result.rowsProcessed} rows`);
});

sync.on('sync-error', (error) => {
  console.error('Sync error:', error);
});
```

### sync.transform(table, fn)

Register a transformation function for a table.

```javascript
sync.transform('users', (row) => {
  return {
    ...row,
    email: row.email.toLowerCase(),
    synced_at: new Date()
  };
});
```

### sync.on(event, handler)

Listen to sync events.

**Events:**
- `sync-start`: Sync cycle begins
- `sync-complete`: Sync cycle finished successfully
- `sync-error`: Sync failed
- `table-sync-start`: Individual table sync begins
- `table-sync-complete`: Individual table sync finished

## Monitoring

DataSync exposes Prometheus-compatible metrics:

```javascript
const express = require('express');
const app = express();

app.get('/metrics', (req, res) => {
  res.set('Content-Type', sync.metrics.contentType());
  res.end(sync.metrics.register.metrics());
});
```

**Available metrics:**
- `datasync_rows_synced_total`: Total rows synced
- `datasync_sync_duration_seconds`: Sync duration
- `datasync_errors_total`: Total errors
- `datasync_conflicts_total`: Total conflicts encountered

## Common Patterns

### One-way sync to a read replica

```javascript
const sync = new DataSync({
  source: { type: 'postgres', connection: productionDb },
  destination: { type: 'postgres', connection: readReplicaDb },
  tables: [...]
});

sync.watch({ interval: 30000 }); // Sync every 30 seconds
```

### Multi-destination sync

```javascript
const mongoSync = new DataSync({
  source: { type: 'postgres', connection: productionDb },
  destination: { type: 'mongodb', connection: mongoUrl },
  tables: [...]
});

const redisSync = new DataSync({
  source: { type: 'postgres', connection: productionDb },
  destination: { type: 'redis', connection: redisUrl },
  tables: [...]
});

// Run both
Promise.all([mongoSync.run(), redisSync.run()]);
```

## Performance Considerations

- **Batch size:** Large tables are synced in batches. Default batch size is 1000 rows. Adjust with `batchSize` option.
- **Parallelism:** Multiple tables can sync in parallel. Set `maxConcurrent` to control concurrency (default: 3).
- **Indexes:** Ensure indexes exist on primary key and sync key columns in both source and destination.
- **Transaction scope:** Large syncs are wrapped in transactions. Very large tables may need manual batching.

## Troubleshooting

**Sync is slow**
- Check that indexes exist on syncKey columns
- Reduce batch size if transactions are timing out
- Monitor destination database load—writes may be bottlenecked

**Frequent conflicts**
- Review conflict resolution strategy
- Check if source and destination are receiving concurrent writes

**Memory usage grows during sync**
- Reduce batch size
- Check that connection pooling is configured
- Monitor for connection leaks

## License

MIT

## Contributing

Issues and pull requests welcome. Please include tests for new features.

## Support

For questions or issues, open a GitHub issue or check the FAQ in the wiki.