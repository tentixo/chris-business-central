# Vert.x Hard Rules (Foundation)

**Scope**: Vert.x-specific rules for TXO projects
**Version**: 1.0
**Extracted from**: txo-java-vertx-adr_v1.0.md
**Updated**: 2026-01-04

---

## MUST (Required)

### VERTX-MUST-1: Never Block Event Loop
- MUST NOT execute blocking operations on event loop thread
- MUST use `executeBlocking()` for short blocking ops (<100ms)
- MUST use worker verticle for long blocking ops (JDBC, heavy I/O)
- MUST use worker verticle for CPU-intensive operations

**Detection**: Vert.x logs warning when blocked:
```
Thread vertx-eventloop-thread-0 has been blocked for 2000 ms
```

Source: ADR-V002

### VERTX-MUST-2: Blocking in Separate Verticle
- MUST NOT mix blocking and non-blocking code in same verticle
- MUST deploy blocking operations as worker verticles
- MUST use event bus to communicate between standard and worker verticles
```java
// ✅ CORRECT - Worker verticle for blocking
public class LdapWorkerVerticle extends AbstractVerticle {
    // Deploy with: new DeploymentOptions().setWorker(true)

    @Override
    public void start() {
        vertx.eventBus().consumer("ldap.lookup", this::handleLookup);
    }

    private void handleLookup(Message<JsonObject> message) {
        // OK to block here - it's a worker
        Certificate cert = ldapClient.lookup(message.body().getString("email"));
        message.reply(cert.toJson());
    }
}

// ❌ WRONG - Blocking on event loop
public void processMessage(Message<JsonObject> message) {
    byte[] data = Files.readAllBytes(path);  // BLOCKS EVENT LOOP!
    Thread.sleep(1000);  // NEVER on event loop!
}
```
Source: ADR-V002, user requirement

### VERTX-MUST-3: Futures Over Callbacks
- MUST use Future/Promise patterns for async operations
- MUST NOT use callback-style APIs when Future alternatives exist
```java
// ✅ CORRECT - Future composition
public Future<JsonObject> fetchAndProcess(String id) {
    return vertx.eventBus()
        .<JsonObject>request("service.fetch", id)
        .compose(reply -> processData(reply.body()))
        .compose(processed -> saveToDatabase(processed));
}

// ❌ WRONG - Callback hell
public void fetchAndProcess(String id, Handler<AsyncResult<JsonObject>> handler) {
    vertx.eventBus().request("service.fetch", id, reply -> {
        if (reply.succeeded()) {
            processData(reply.result().body(), processResult -> {
                // Nesting continues...
            });
        }
    });
}
```
Source: ADR-V001

### VERTX-MUST-4: Verticle Lifecycle
- MUST return Future from start() method
- MUST clean up resources in stop() method
- MUST deploy dependencies before dependents
```java
@Override
public void start(Promise<Void> startPromise) {
    initializeDependencies()
        .compose(v -> registerHandlers())
        .onSuccess(v -> startPromise.complete())
        .onFailure(startPromise::fail);
}

@Override
public void stop(Promise<Void> stopPromise) {
    unregisterHandlers()
        .compose(v -> closeDependencies())
        .onComplete(result -> stopPromise.complete());
}
```
Source: ADR-V003

### VERTX-MUST-5: Event Bus Failure Handling
- MUST handle failure cases in event bus replies
- MUST NOT assume success
```java
// ✅ CORRECT - Handle failures
vertx.eventBus().<JsonObject>request("service.action", data)
    .onSuccess(reply -> processResult(reply.body()))
    .onFailure(err -> logger.error("Request failed", err));

// ❌ WRONG - Assuming success
vertx.eventBus().request("service.action", data, reply -> {
    JsonObject result = reply.result().body();  // NPE if failed!
});
```
Source: ADR-V004

---

## MUST NOT (Forbidden)

### VERTX-MUSTNOT-1: Blocking Calls on Event Loop
```java
// ❌ NEVER on event loop
Files.readAllBytes(path);           // Blocks!
Thread.sleep(1000);                 // Blocks!
synchronousHttpClient.get(url);     // Blocks!
jdbcConnection.executeQuery(sql);   // Blocks!
```
Source: ADR-V002

### VERTX-MUSTNOT-2: Mixed Blocking/Non-Blocking Verticle
- MUST NOT have both blocking and non-blocking handlers in same verticle
Source: user requirement

---

## SHOULD (Recommended)

### VERTX-SHOULD-1: Event Bus Address Naming
```
{service}.{action}[.{subtype}]

Examples:
- e1.email.process       # E1 process email
- e1.cert.lookup         # E1-Cert lookup certificate
- v1.validate.prodat     # V1 validate PRODAT message
```
Source: ADR-V004

### VERTX-SHOULD-2: Verticle Code Structure Order
1. Logger
2. Constants (static final)
3. Instance fields
4. Lifecycle methods (start, stop)
5. Initialization helpers
6. Event bus handlers
7. Business logic methods
8. Config helpers
Source: ADR-V006

### VERTX-SHOULD-3: Handler Naming Convention
| Element | Convention | Example |
|---------|------------|---------|
| Address constants | `ADDRESS_*` | `ADDRESS_LOOKUP` |
| Handler methods | `handle*` | `handleLookup` |
| Init methods | `initialize*` | `initializeDependencies` |
| Cleanup methods | `close*`/`unregister*` | `closeDependencies` |
Source: ADR-V006

---

## Quick Reference

| Category | Key Rules |
|----------|-----------|
| Event Loop | NEVER block, use workers for blocking |
| Async | Futures over callbacks, always handle failures |
| Lifecycle | Return Future from start(), cleanup in stop() |
| Structure | Separate blocking into worker verticles |
| Naming | Dot-separated addresses, handle* methods |
