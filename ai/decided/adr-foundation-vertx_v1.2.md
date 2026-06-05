# TXO Java Vert.x Architecture Decision Records v1.1

These ADRs define **Vert.x-specific patterns** for TXO Java projects. For base Java patterns (config, logging, naming),
see `adr-foundation-java_v1.1.md`.

**Status**: Living document - grows iteratively  
**Created**: 2026-01-02  
**Updated**: 2026-01-04 (v1.1 - async DB patterns, virtual threads)  
**Prerequisite**: `adr-foundation-java_v1.3.md` (base patterns)

---

## ADR-V001: Future Over Callbacks

**Status:** MANDATORY
**Date:** 2026-01-02

### Context

Vert.x 5 supports both callback-style and Future-based async. Callbacks lead to "callback hell" and are harder to
compose.

### Decision

**Always use Future/Promise patterns.** Never use callback-style APIs when Future alternatives exist.

### Implementation

```java
// ✅ CORRECT - Future composition
public Future<JsonObject> fetchAndProcess(String id) {
    return vertx.eventBus()
        .<JsonObject>request("service.fetch", id)
        .compose(reply -> {
            JsonObject data = reply.body();
            return processData(data);
        })
        .compose(processed -> saveToDatabase(processed))
        .onSuccess(result -> logger.info("Completed: {}", id))
        .onFailure(err -> logger.error("Failed: {}", id, err));
}

// ✅ CORRECT - Promise for async operations
public Future<Void> initialize() {
    Promise<Void> promise = Promise.promise();

    someAsyncOperation(result -> {
        if (result.succeeded()) {
            promise.complete();
        } else {
            promise.fail(result.cause());
        }
    });

    return promise.future();
}

// ❌ WRONG - Callback style
public void fetchAndProcess(String id, Handler<AsyncResult<JsonObject>> handler) {
    vertx.eventBus().request("service.fetch", id, reply -> {
        if (reply.succeeded()) {
            processData(reply.result().body(), processResult -> {
                if (processResult.succeeded()) {
                    // Callback hell continues...
                }
            });
        }
    });
}
```

### Future Composition Patterns

| Method          | Use Case                                  |
|-----------------|-------------------------------------------|
| `.compose()`    | Chain dependent async operations          |
| `.map()`        | Transform success value synchronously     |
| `.recover()`    | Handle failure, return alternative Future |
| `.otherwise()`  | Handle failure, return default value      |
| `.onComplete()` | Final handler (both success/failure)      |

### Consequences

- Positive: Readable code, easy composition, better error handling
- Negative: Learning curve for callback-trained developers
- Mitigation: Clear examples, IDE support for Future methods

---

## ADR-V002: Blocking vs Non-Blocking

**Status:** MANDATORY
**Date:** 2026-01-02

### Context

Vert.x event loop must never block. Blocking operations (file I/O, JDBC, CPU-intensive) require special handling.

### Decision

| Operation                                  | Approach                          |
|--------------------------------------------|-----------------------------------|
| **Quick async** (event bus, async clients) | Run directly on event loop        |
| **Short blocking** (<100ms, occasional)    | `executeBlocking()`               |
| **Long blocking** (JDBC, heavy I/O)        | Worker verticle or dedicated pool |
| **CPU-intensive**                          | Worker verticle                   |

### Implementation

```java
// ✅ CORRECT - Short blocking operation
public Future<byte[]> readSmallFile(String path) {
    return vertx.executeBlocking(() -> {
        return Files.readAllBytes(Path.of(path));
    });
}

// ✅ CORRECT - Couchbase async client (non-blocking)
public Future<JsonDocument> fetchDocument(String id) {
    return Future.fromCompletionStage(
        couchbaseCollection.get(id).toFuture()
    ).map(result -> result.contentAsObject());
}

// ✅ CORRECT - Worker verticle for heavy operations
public class HeavyProcessingVerticle extends AbstractVerticle {
    // Deploy with worker option
    // new DeploymentOptions().setWorker(true)

    @Override
    public void start() {
        vertx.eventBus().consumer("heavy.process", this::handleHeavyWork);
    }

    private void handleHeavyWork(Message<JsonObject> message) {
        // OK to block here - it's a worker
        JsonObject result = expensiveComputation(message.body());
        message.reply(result);
    }
}

// ❌ WRONG - Blocking on event loop
public void processMessage(Message<JsonObject> message) {
    byte[] data = Files.readAllBytes(path);  // BLOCKS EVENT LOOP!
    Thread.sleep(1000);  // NEVER do this on event loop!
}
```

### Detecting Blocked Event Loop

Vert.x logs warnings when event loop is blocked:

```
Thread vertx-eventloop-thread-0 has been blocked for 2000 ms
```

Enable checker in development:

```java
VertxOptions options = new VertxOptions()
    .setBlockedThreadCheckInterval(1000);
```

### Consequences

- Positive: Responsive application, high throughput
- Negative: Must categorize all operations
- Mitigation: Use async clients (Couchbase, HTTP), worker verticles

---

## ADR-V003: Verticle Lifecycle

**Status:** MANDATORY
**Date:** 2026-01-02

### Context

Verticles are Vert.x deployment units. Proper lifecycle management ensures clean startup and shutdown.

### Decision

- **start()**: Initialize resources, return Future
- **stop()**: Cleanup resources, close connections
- **Deployment order**: Deploy dependencies first (compose Futures)

### Implementation

```java
public class E1ReceiveVerticle extends AbstractVerticle {

    private static final Logger logger = LoggerFactory.getLogger(E1ReceiveVerticle.class);
    private MessageConsumer<JsonObject> consumer;
    private CouchbaseCluster couchbase;

    @Override
    public void start(Promise<Void> startPromise) {
        logger.info("Starting E1ReceiveVerticle");

        // Initialize resources
        initializeCouchbase()
            .compose(v -> registerEventBusHandlers())
            .onSuccess(v -> {
                logger.info("E1ReceiveVerticle started");
                startPromise.complete();
            })
            .onFailure(err -> {
                logger.error("Failed to start E1ReceiveVerticle", err);
                startPromise.fail(err);
            });
    }

    @Override
    public void stop(Promise<Void> stopPromise) {
        logger.info("Stopping E1ReceiveVerticle");

        // Unregister handlers first
        Future<Void> unregister = consumer != null
            ? consumer.unregister()
            : Future.succeededFuture();

        // Then close connections
        unregister
            .compose(v -> closeCouchbase())
            .onComplete(result -> {
                logger.info("E1ReceiveVerticle stopped");
                stopPromise.complete();  // Complete even if cleanup fails
            });
    }

    private Future<Void> initializeCouchbase() {
        return vertx.executeBlocking(() -> {
            couchbase = CouchbaseCluster.connect(/* ... */);
            return null;
        });
    }

    private Future<Void> registerEventBusHandlers() {
        consumer = vertx.eventBus().consumer("e1.process", this::handleMessage);
        return consumer.completionHandler();
    }
}
```

### Deployment Order Pattern

```java
// MainVerticle - orchestrate deployment order
@Override
public void start(Promise<Void> startPromise) {
    // Deploy dependencies first
    vertx.deployVerticle(new E1CertVerticle())
        .compose(certId -> {
            logger.info("E1-Cert deployed: {}", certId);
            // Then deploy dependent verticle
            return vertx.deployVerticle(new E1ReceiveVerticle());
        })
        .compose(emailId -> {
            logger.info("E1-Receive deployed: {}", emailId);
            return Future.succeededFuture();
        })
        .onSuccess(v -> startPromise.complete())
        .onFailure(startPromise::fail);
}
```

### Consequences

- Positive: Clean startup/shutdown, proper resource management
- Negative: More verbose than simple main()
- Mitigation: Base verticle class with common patterns

---

## ADR-V004: Event Bus Patterns

**Status:** MANDATORY
**Date:** 2026-01-02

### Context

Vert.x event bus enables decoupled communication between verticles. Consistent patterns prevent confusion.

### Decision

- **Addresses**: Dot-separated, hierarchical (`service.action.subtype`)
- **Point-to-point**: `request()` for RPC-style calls
- **Publish/subscribe**: `publish()` for notifications
- **Always handle failures**: Check reply status

### Address Naming Convention

```
{service}.{action}[.{subtype}]

Examples:
- e1.email.process       # E1 process email
- e1.cert.lookup         # E1-Cert lookup certificate
- v1.validate.prodat     # V1 validate PRODAT message
- notify.email.sent      # Notification (pub/sub)
```

### Implementation

```java
// ✅ CORRECT - Request/Reply pattern
public Future<JsonObject> lookupCertificate(String email) {
    return vertx.eventBus()
        .<JsonObject>request("e1.cert.lookup", new JsonObject().put("email", email))
        .map(Message::body)
        .onFailure(err -> logger.error("Cert lookup failed for {}", email, err));
}

// ✅ CORRECT - Publish notification (no reply expected)
public void notifyEmailProcessed(String messageId) {
    vertx.eventBus().publish("notify.email.processed",
        new JsonObject()
            .put("messageId", messageId)
            .put("timestamp", Instant.now().toString())
    );
}

// ✅ CORRECT - Consumer registration
public void registerHandlers() {
    vertx.eventBus().<JsonObject>consumer("e1.email.process", message -> {
        JsonObject request = message.body();

        processEmail(request)
            .onSuccess(result -> message.reply(result))
            .onFailure(err -> message.fail(500, err.getMessage()));
    });
}

// ❌ WRONG - Not handling failure
vertx.eventBus().request("service.action", data, reply -> {
    // Assuming success - what if reply.failed()?
    JsonObject result = reply.result().body();
});
```

### Consequences

- Positive: Decoupled services, scalable, testable
- Negative: Indirect communication harder to trace
- Mitigation: Consistent naming, logging with correlation IDs

---

## ADR-V005: Configuration with JsonObject

**Status:** MANDATORY
**Date:** 2026-01-02

### Context

Vert.x uses JsonObject for configuration. This must integrate with ADR-J006 (config/secrets file structure) and
vertx-config.

### Decision

- Use Vert.x JsonObject for configuration passing
- Load config per ADR-J006 structure: `config/{module}/{env}-config.json`
- Use vertx-config with multiple stores (shared + module + secrets)
- Apply ADR-J001 (hard-fail) when accessing config values

### Implementation

**Config Loading with ADR-J006 Structure:**

```java
/**
 * Loads configuration per ADR-J006 structure.
 * Files: config/shared/{env}-config.json, config/{module}/{env}-config.json
 * Secrets: config/shared/{env}-config-secrets.json, config/{module}/{env}-config-secrets.json
 */
public Future<JsonObject> loadModuleConfig(Vertx vertx, String env, String moduleName) {
    ConfigRetrieverOptions options = new ConfigRetrieverOptions()
        // Load in order: shared config, shared secrets, module config, module secrets
        // Later stores override earlier ones
        .addStore(fileStore("config/shared/" + env + "-config.json"))
        .addStore(fileStore("config/shared/" + env + "-config-secrets.json"))
        .addStore(fileStore("config/" + moduleName + "/" + env + "-config.json"))
        .addStore(fileStore("config/" + moduleName + "/" + env + "-config-secrets.json"));

    return ConfigRetriever.create(vertx, options).getConfig();
}

private ConfigStoreOptions fileStore(String path) {
    return new ConfigStoreOptions()
        .setType("file")
        .setFormat("json")
        .setOptional(true)  // Secrets file may not exist in dev
        .setConfig(new JsonObject().put("path", path));
}
```

**Deploy Verticle with Config:**

```java
// In MainVerticle
String env = System.getenv().getOrDefault("APP_ENV", "dev");

loadModuleConfig(vertx, env, "e1-cert")
    .compose(config -> {
        DeploymentOptions options = new DeploymentOptions().setConfig(config);
        return vertx.deployVerticle(new E1CertVerticle(), options);
    })
    .onSuccess(id -> logger.info("E1-Cert deployed: {}", id))
    .onFailure(err -> logger.error("Failed to deploy E1-Cert", err));
```

**Access Config in Verticle (hard-fail per ADR-J001):**

```java
@Override
public void start(Promise<Void> startPromise) {
    JsonObject config = config();  // Vert.x provides merged config

    // Hard-fail on missing required config
    String ldapUrl = getRequired(config, "ldap-url");
    int cacheTtlHours = getRequiredInt(config, "cache-ttl-hours");
    String certPassword = getRequired(config, "signing-cert-password");  // From secrets

    // Continue initialization...
}

private String getRequired(JsonObject config, String key) {
    String value = config.getString(key);
    if (value == null) {
        throw new IllegalStateException("Missing required config: " + key);
    }
    return value;
}

private int getRequiredInt(JsonObject config, String key) {
    Integer value = config.getInteger(key);
    if (value == null) {
        throw new IllegalStateException("Missing required config: " + key);
    }
    return value;
}
```

### Consequences

- Positive: Native Vert.x integration, follows ADR-J006 structure
- Positive: Secrets loaded separately (gitignored files)
- Negative: Runtime type checking (no compile-time safety)
- Mitigation: Validate config at startup with `getRequired()` helpers

---

## ADR-V006: Verticle Code Structure

**Status:** RECOMMENDED
**Date:** 2026-01-02

### Context

Consistent verticle structure improves readability and maintainability. Developers should know where to find
initialization, handlers, and cleanup code.

### Decision

Organize verticle code in this order:

1. **Class declaration & logger**
2. **Constants** (static final)
3. **Instance fields** (dependencies, state)
4. **Lifecycle methods** (start, stop)
5. **Initialization helpers** (private, called from start)
6. **Event bus handlers** (private, registered in start)
7. **Business logic methods** (private/package)
8. **Config helper methods** (private, at bottom)

### Implementation

```java
public class E1CertVerticle extends AbstractVerticle {

    // 1. Logger
    private static final Logger logger = LoggerFactory.getLogger(E1CertVerticle.class);

    // 2. Constants
    private static final String ADDRESS_LOOKUP = "e1.cert.lookup";
    private static final int DEFAULT_CACHE_TTL_HOURS = 24;

    // 3. Instance fields - dependencies
    private CertificateCache cache;
    private LdapClient ldapClient;
    private MessageConsumer<JsonObject> lookupConsumer;

    // 4. Lifecycle - start
    @Override
    public void start(Promise<Void> startPromise) {
        logger.info("Starting E1CertVerticle");

        initializeFromConfig()
            .compose(v -> initializeDependencies())
            .compose(v -> registerHandlers())
            .onSuccess(v -> {
                logger.info("E1CertVerticle started");
                startPromise.complete();
            })
            .onFailure(err -> {
                logger.error("Failed to start E1CertVerticle", err);
                startPromise.fail(err);
            });
    }

    // 4. Lifecycle - stop
    @Override
    public void stop(Promise<Void> stopPromise) {
        logger.info("Stopping E1CertVerticle");

        unregisterHandlers()
            .compose(v -> closeDependencies())
            .onComplete(result -> {
                logger.info("E1CertVerticle stopped");
                stopPromise.complete();
            });
    }

    // 5. Initialization helpers
    private Future<Void> initializeFromConfig() {
        JsonObject config = config();
        // Validate and extract config...
        return Future.succeededFuture();
    }

    private Future<Void> initializeDependencies() {
        // Initialize cache, LDAP client, etc.
        return Future.succeededFuture();
    }

    private Future<Void> registerHandlers() {
        lookupConsumer = vertx.eventBus().consumer(ADDRESS_LOOKUP, this::handleLookup);
        return lookupConsumer.completionHandler();
    }

    private Future<Void> unregisterHandlers() {
        return lookupConsumer != null
            ? lookupConsumer.unregister()
            : Future.succeededFuture();
    }

    private Future<Void> closeDependencies() {
        // Close connections...
        return Future.succeededFuture();
    }

    // 6. Event bus handlers
    private void handleLookup(Message<JsonObject> message) {
        String email = message.body().getString("email");

        lookupCertificate(email)
            .onSuccess(cert -> message.reply(cert))
            .onFailure(err -> message.fail(500, err.getMessage()));
    }

    // 7. Business logic
    private Future<JsonObject> lookupCertificate(String email) {
        // Business logic here...
        return Future.succeededFuture(new JsonObject());
    }

    // 8. Config helpers (at bottom)
    private String getRequired(JsonObject config, String key) {
        String value = config.getString(key);
        if (value == null) {
            throw new IllegalStateException("Missing config: " + key);
        }
        return value;
    }
}
```

### Naming Conventions

| Element                     | Convention                | Example                                   |
|-----------------------------|---------------------------|-------------------------------------------|
| Event bus address constants | `ADDRESS_*`               | `ADDRESS_LOOKUP`, `ADDRESS_PROCESS`       |
| Handler methods             | `handle*`                 | `handleLookup`, `handleProcess`           |
| Init methods                | `initialize*` or `init*`  | `initializeDependencies`                  |
| Cleanup methods             | `close*` or `unregister*` | `closeDependencies`, `unregisterHandlers` |

### Consequences

- Positive: Consistent structure, easy to navigate
- Positive: Clear separation of lifecycle, handlers, and logic
- Negative: Slightly more verbose
- Mitigation: IDE templates, copy from existing verticles

---

## ADR-V007: Async Database Integration

**Status:** MANDATORY
**Date:** 2026-01-04

### Context

Modern database SDKs (Couchbase, Redis, etc.) provide async APIs that must integrate cleanly with Vert.x's Future-based
model. This pattern is generic across database clients.

### Decision

Use this pattern for any async database client:

| SDK Returns            | Vert.x Conversion                                           |
|------------------------|-------------------------------------------------------------|
| `CompletableFuture<T>` | `Future.fromCompletionStage(cf)`                            |
| `Mono<T>` (Reactor)    | `Future.fromCompletionStage(mono.toFuture())`               |
| `Flux<T>` (Reactor)    | `Future.fromCompletionStage(flux.collectList().toFuture())` |
| Callback-based         | Wrap in `Promise`                                           |

### Implementation

**Couchbase Example (CompletableFuture):**

```java
public class CouchbaseRepository {
    private final AsyncCollection collection;

    // Async API returns CompletableFuture
    public Future<JsonObject> getDocument(String id) {
        return Future.fromCompletionStage(
            collection.get(id)
        ).map(result -> {
            return new JsonObject(result.contentAsObject().toMap());
        });
    }

    public Future<Void> upsertDocument(String id, JsonObject doc) {
        return Future.fromCompletionStage(
            collection.upsert(id, doc.getMap())
        ).mapEmpty();
    }
}
```

**Reactive API (Reactor Mono/Flux):**

```java
public class ReactiveRepository {
    private final ReactiveCollection collection;

    // Reactive API returns Mono
    public Future<JsonObject> getDocument(String id) {
        return Future.fromCompletionStage(
            collection.get(id).toFuture()
        ).map(result -> new JsonObject(result.contentAsObject().toMap()));
    }

    // Flux to List
    public Future<List<JsonObject>> queryDocuments(String query) {
        return Future.fromCompletionStage(
            collection.scan(ScanType.SAMPLE)
                .map(result -> new JsonObject(result.contentAsObject().toMap()))
                .collectList()
                .toFuture()
        );
    }
}
```

**Generic Pattern (Any Async Client):**

```java
public class AsyncClientAdapter {

    // Pattern: Wrap CompletableFuture-returning method
    public <T> Future<T> toVertxFuture(CompletableFuture<T> cf) {
        return Future.fromCompletionStage(cf);
    }

    // Pattern: Wrap callback-based API
    public Future<Result> wrapCallback(Consumer<AsyncCallback<Result>> operation) {
        Promise<Result> promise = Promise.promise();
        operation.accept(new AsyncCallback<Result>() {
            @Override
            public void onSuccess(Result result) {
                promise.complete(result);
            }

            @Override
            public void onError(Throwable t) {
                promise.fail(t);
            }
        });
        return promise.future();
    }
}
```

### Three API Levels

Most modern SDKs provide three API levels:

| API          | Returns             | Use When                        |
|--------------|---------------------|---------------------------------|
| **Sync**     | Direct value        | Worker verticle, simple scripts |
| **Async**    | `CompletableFuture` | Standard Vert.x integration     |
| **Reactive** | `Mono`/`Flux`       | Complex streaming, backpressure |

**Recommendation**: Use **Async** (CompletableFuture) for most cases. It integrates cleanly with Vert.x Futures.

### Error Handling

```java
public Future<JsonObject> getDocumentSafe(String id) {
    return Future.fromCompletionStage(collection.get(id))
        .map(result -> new JsonObject(result.contentAsObject().toMap()))
        .recover(err -> {
            if (err instanceof DocumentNotFoundException) {
                return Future.succeededFuture(null);  // Document not found is OK
            }
            logger.error("Database error fetching {}", id, err);
            return Future.failedFuture(err);
        });
}
```

### Consequences

- Positive: Clean integration with Vert.x Future chains
- Positive: Pattern applies to any async SDK
- Negative: Type conversion overhead (minimal)
- Mitigation: Repository abstraction hides conversion details

---

## ADR-V008: Virtual Threads with Vert.x

**Status:** RECOMMENDED
**Date:** 2026-01-04

### Context

Java 21 virtual threads provide lightweight threads for blocking operations. Vert.x 5 replaced "Vert.x Sync" with "
Vert.x virtual threads" module. However, virtual threads must be used carefully with Vert.x's event loop model.

### Decision

| Use Case                | Approach              | Why                                  |
|-------------------------|-----------------------|--------------------------------------|
| **Event loop verticle** | Standard Vert.x async | Event loop already efficient         |
| **Worker verticle**     | Virtual threads OK    | Workers already for blocking         |
| **Blocking library**    | Virtual threads       | Better than platform threads         |
| **CPU-intensive**       | Worker pool           | Virtual threads don't help CPU-bound |

**Key insight**: Virtual threads excel at I/O-bound blocking operations. Vert.x event loop already handles async I/O
efficiently. Use virtual threads when you MUST use blocking APIs.

### Implementation

**Worker Verticle with Virtual Threads:**

```java
// Deploy with virtual thread executor
DeploymentOptions options = new DeploymentOptions()
    .setWorkerPoolName("ldap-workers")
    .setWorkerPoolSize(100)  // Virtual threads can be many
    .setWorker(true);

vertx.deployVerticle(new LdapWorkerVerticle(), options);
```

**Execute Blocking with Virtual Threads:**

```java
// Vert.x 5+ with virtual threads module
import io.vertx.core.ThreadingModel;

// Use virtual thread for blocking operation
public Future<Certificate> lookupCertificateBlocking(String email) {
    return vertx.executeBlocking(() -> {
        // This blocking LDAP call runs on virtual thread
        return ldapClient.lookup(email);
    }, false);  // false = unordered (can run in parallel)
}
```

**Structured Concurrency (Java 21):**

```java
// When you need multiple blocking calls in parallel
public Future<CertificateResult> lookupMultiple(List<String> emails) {
    return vertx.executeBlocking(() -> {
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
            List<Subtask<Certificate>> tasks = emails.stream()
                .map(email -> scope.fork(() -> ldapClient.lookup(email)))
                .toList();

            scope.join();
            scope.throwIfFailed();

            return new CertificateResult(
                tasks.stream()
                    .map(Subtask::get)
                    .toList()
            );
        }
    });
}
```

### When NOT to Use Virtual Threads

| Scenario              | Why Not                               | Alternative        |
|-----------------------|---------------------------------------|--------------------|
| Event loop code       | Already async, no blocking            | Normal Vert.x      |
| Async database client | Client handles async                  | Future composition |
| CPU-intensive work    | Virtual threads don't parallelize CPU | Worker pool        |
| Thread-local state    | Virtual threads may migrate           | Vert.x context     |

### Migration from Worker Verticles

If you have worker verticles for blocking operations:

```java
// Before: Platform thread worker
new DeploymentOptions().setWorker(true)

// After: Virtual thread worker (Vert.x 5+)
new DeploymentOptions()
    .setThreadingModel(ThreadingModel.VIRTUAL_THREAD)
```

### Consequences

- Positive: Better resource utilization for blocking code
- Positive: Can handle more concurrent blocking operations
- Negative: Must understand when NOT to use them
- Mitigation: Use only for blocking APIs that have no async alternative

---

## ADR-V009: Circuit Breaker Pattern

**Status:** MANDATORY
**Date:** 2026-01-04

### Context

External services (LDAP, IMAP, APIs) can fail or become slow. Without circuit breakers, failures cascade and slow down
the entire system.

### Decision

**MUST** use circuit breaker for all external service calls.
Vert.x provides built-in circuit breaker support via `vertx-circuit-breaker`.

### Implementation

```java
import io.vertx.circuitbreaker.CircuitBreaker;
import io.vertx.circuitbreaker.CircuitBreakerOptions;

public class LdapClient {
    private final CircuitBreaker circuitBreaker;

    public LdapClient(Vertx vertx) {
        this.circuitBreaker = CircuitBreaker.create("ldap-breaker", vertx,
            new CircuitBreakerOptions()
                .setMaxFailures(5)           // Open after 5 failures
                .setTimeout(10000)           // 10s timeout per call
                .setResetTimeout(30000)      // Try again after 30s
                .setFallbackOnFailure(true)  // Use fallback when open
        );
    }

    public Future<Certificate> lookup(String email) {
        return circuitBreaker.execute(promise -> {
            // Actual LDAP lookup
            doLdapLookup(email)
                .onSuccess(promise::complete)
                .onFailure(promise::fail);
        }).recover(err -> {
            // Fallback: return cached or error
            logger.warn("LDAP circuit open, using fallback for {}", email);
            return getCachedCertificate(email);
        });
    }
}
```

### Circuit States

| State         | Behavior                              | Transitions                            |
|---------------|---------------------------------------|----------------------------------------|
| **CLOSED**    | Normal operation, calls go through    | → OPEN after max failures              |
| **OPEN**      | Calls fail immediately, fallback used | → HALF-OPEN after reset timeout        |
| **HALF-OPEN** | Single call allowed to test           | → CLOSED on success, → OPEN on failure |

### Configuration Guidelines

| Service Type     | Max Failures | Timeout | Reset Timeout |
|------------------|--------------|---------|---------------|
| **LDAP**         | 5            | 10s     | 30s           |
| **IMAP**         | 3            | 30s     | 60s           |
| **External API** | 5            | 5s      | 30s           |
| **Database**     | 3            | 5s      | 10s           |

### Consequences

- Positive: Prevents cascade failures, fast failure when service down
- Positive: Automatic recovery when service returns
- Negative: Must implement fallback logic
- Mitigation: Cache, queue, or graceful degradation

---

## ADR-V010: Error Response Strategy

**Status:** MANDATORY
**Date:** 2026-01-04

### Context

When an operation fails, should the error be in:

- HTTP status code (4xx/5xx)?
- HTTP 200 with error in payload?

Different contexts need different approaches.

### Decision

**Use HTTP status codes for transport-level errors.**
**Use HTTP 200 + payload for business-level results that include partial success or expected failures.**

### Implementation

#### Transport-Level Errors → HTTP Status Codes

```java
// ✅ CORRECT - Use HTTP status for transport/auth failures
router.get("/api/cert/:email").handler(ctx -> {
    String email = ctx.pathParam("email");

    lookupCertificate(email)
        .onSuccess(cert -> {
            ctx.response()
                .setStatusCode(200)
                .putHeader("Content-Type", "application/json")
                .end(cert.encode());
        })
        .onFailure(err -> {
            if (err instanceof NotFoundException) {
                ctx.response().setStatusCode(404)
                    .end(errorJson("Certificate not found"));
            } else if (err instanceof AuthenticationException) {
                ctx.response().setStatusCode(401)
                    .end(errorJson("Authentication required"));
            } else {
                ctx.response().setStatusCode(500)
                    .end(errorJson("Internal error"));
            }
        });
});
```

#### Business Results → HTTP 200 + Payload

```java
// ✅ CORRECT - Use 200 + payload for business results with details
router.post("/api/validate-batch").handler(ctx -> {
    JsonArray messages = ctx.body().asJsonArray();

    validateBatch(messages)
        .onSuccess(results -> {
            // Some may have succeeded, some failed - still 200
            JsonObject response = new JsonObject()
                .put("status", "completed")
                .put("total", messages.size())
                .put("valid", results.validCount())
                .put("invalid", results.invalidCount())
                .put("errors", results.errors());  // Details inline

            ctx.response()
                .setStatusCode(200)
                .end(response.encode());
        });
});
```

### Decision Matrix

| Scenario                   | HTTP Status | Payload Contains          |
|----------------------------|-------------|---------------------------|
| Success                    | 200         | Result data               |
| Not found                  | 404         | Error message             |
| Auth failure               | 401         | Error message             |
| Validation error (request) | 400         | Validation errors         |
| Partial success (batch)    | **200**     | Success + failure details |
| Expected business failure  | **200**     | Status + reason           |
| Unexpected error           | 500         | Error message (sanitized) |

### Event Bus Pattern

For event bus messages, always use reply with status:

```java
// Event bus handler
private void handleLookup(Message<JsonObject> message) {
    String email = message.body().getString("email");

    lookupCertificate(email)
        .onSuccess(cert -> {
            message.reply(new JsonObject()
                .put("status", "success")
                .put("certificate", cert));
        })
        .onFailure(err -> {
            if (err instanceof NotFoundException) {
                // Expected failure - reply with status
                message.reply(new JsonObject()
                    .put("status", "not_found")
                    .put("reason", "Certificate not found for " + email));
            } else {
                // Unexpected failure - fail the message
                message.fail(500, err.getMessage());
            }
        });
}
```

### Consequences

- Positive: Clear distinction between transport and business errors
- Positive: Clients can handle partial success gracefully
- Negative: Must decide which category each error falls into
- Mitigation: Decision matrix above, team conventions

---

## ADR-V011: Graceful Startup and Shutdown

**Status:** MANDATORY
**Date:** 2026-01-04

### Context

Beyond individual verticle lifecycle, the application needs graceful startup (wait for dependencies) and shutdown (drain
connections, complete in-flight work).

### Decision

**MUST** implement app-level graceful startup and shutdown.
**MUST** register shutdown hook for container/k8s termination.

### Implementation

#### Graceful Startup

```java
public class MainVerticle extends AbstractVerticle {

    @Override
    public void start(Promise<Void> startPromise) {
        // 1. Wait for external dependencies
        waitForDependencies()
            // 2. Deploy verticles in order
            .compose(v -> deployVerticlesInOrder())
            // 3. Register health endpoint
            .compose(v -> registerHealthEndpoint())
            // 4. Signal ready
            .onSuccess(v -> {
                logger.info("Application started successfully");
                startPromise.complete();
            })
            .onFailure(err -> {
                logger.error("Application startup failed", err);
                startPromise.fail(err);
            });
    }

    private Future<Void> waitForDependencies() {
        return Future.all(
            waitForCouchbase(),
            waitForLdap()
        ).mapEmpty();
    }

    private Future<Void> waitForCouchbase() {
        // Retry connection with backoff
        return retry(5, 2000, () -> couchbaseClient.ping());
    }
}
```

#### Graceful Shutdown

```java
public class MainVerticle extends AbstractVerticle {

    @Override
    public void start(Promise<Void> startPromise) {
        // Register shutdown hook
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            logger.info("Shutdown signal received");
            gracefulShutdown().toCompletionStage().toCompletableFuture().join();
        }));

        // ... rest of startup
    }

    private Future<Void> gracefulShutdown() {
        logger.info("Starting graceful shutdown");

        return Future.succeededFuture()
            // 1. Stop accepting new requests
            .compose(v -> stopHttpServer())
            // 2. Wait for in-flight requests (with timeout)
            .compose(v -> drainInFlight(Duration.ofSeconds(30)))
            // 3. Undeploy verticles in reverse order
            .compose(v -> undeployVerticles())
            // 4. Close external connections
            .compose(v -> closeConnections())
            .onComplete(result -> {
                logger.info("Graceful shutdown complete");
            });
    }

    private Future<Void> drainInFlight(Duration timeout) {
        // Wait for active requests to complete
        Promise<Void> promise = Promise.promise();
        long deadline = System.currentTimeMillis() + timeout.toMillis();

        vertx.setPeriodic(100, timerId -> {
            if (activeRequests.get() == 0) {
                vertx.cancelTimer(timerId);
                promise.complete();
            } else if (System.currentTimeMillis() > deadline) {
                vertx.cancelTimer(timerId);
                logger.warn("Shutdown timeout, {} requests still active", activeRequests.get());
                promise.complete();  // Complete anyway
            }
        });

        return promise.future();
    }
}
```

#### Kubernetes Integration

```yaml
# In deployment.yaml
spec:
  containers:
    - name: numan-edi
      lifecycle:
        preStop:
          exec:
            command: [ "sh", "-c", "sleep 5" ]  # Allow time for load balancer update
      terminationGracePeriodSeconds: 60  # Match drain timeout
```

### Startup/Shutdown Order

```
STARTUP:
1. Wait for external deps (DB, LDAP)
2. Deploy infrastructure verticles (config, health)
3. Deploy worker verticles
4. Deploy HTTP verticles
5. Register with load balancer / set healthy

SHUTDOWN:
1. Unregister from load balancer / set unhealthy
2. Stop accepting new requests
3. Drain in-flight requests (timeout)
4. Undeploy HTTP verticles
5. Undeploy worker verticles
6. Close external connections
```

### Consequences

- Positive: Zero-downtime deployments, no dropped requests
- Positive: Clean state on shutdown
- Negative: More complex startup/shutdown code
- Mitigation: Base class with common patterns

---

## Summary

Vert.x-specific patterns for TXO:

1. **Futures over callbacks**: Compose with `.compose()`, `.map()`, `.recover()`
2. **Never block event loop**: Use `executeBlocking()` or worker verticles
3. **Verticle lifecycle**: Proper start/stop, ordered deployment
4. **Event bus patterns**: Consistent addressing, handle failures
5. **Config with ADR-J006**: Load shared + module config, hard-fail on missing
6. **Verticle code structure**: Consistent ordering (logger, constants, fields, lifecycle, handlers, logic)
7. **Async database integration**: `Future.fromCompletionStage()` for any async SDK
8. **Virtual threads**: Use for blocking APIs only, not for event loop code
9. **Circuit breaker**: Use for all external service calls (LDAP, IMAP, APIs)
10. **Error response strategy**: HTTP status for transport, 200 + payload for business
11. **Graceful startup/shutdown**: Wait for deps, drain in-flight, zero-downtime

Combined with base patterns from `adr-foundation-java_v1.2.md`:

- Hard-fail configuration (ADR-J001)
- Structured logging with context (ADR-J002, ADR-J010)
- Java naming conventions (ADR-J003)
- Gradle multi-module structure (ADR-J004)
- Error handling (ADR-J005)
- Config & secrets structure (ADR-J006)
- Java version management (ADR-J007)
- Java 21 patterns (ADR-J009)
- JSON Schema validation timing (ADR-J011)
- Frontend strategy / HTMX (ADR-J012)
- Variable naming for debuggability (ADR-J013)
- Avoiding singletons (ADR-J014)
- ID generation / UUID v7 (ADR-J015)

---

**Version:** v1.2
**Last Updated:** 2026-01-04
**Domain:** TXO Java Vert.x Architecture
**Purpose:** Vert.x-specific patterns, supplements base Java ADR
